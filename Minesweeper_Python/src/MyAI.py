# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from enum import Enum
import collections
import queue
import copy

class Cell:
    def __init__(self, cell_state, percept, mine_probability, xPos, yPos, adj_cells):
        self.cell_state = cell_state
        self.percept = percept
        self.mine_probability = mine_probability
        self.xPos = xPos
        self.yPos = yPos
        self.isSafe = False
        self.isMine = False
        self.adjCells = adj_cells

class CellState(Enum):
    COVERED = 0
    UNCOVERED = 1
    FLAGGED = 2
    UNFLAGGED = 3

class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startY, startX):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.cellsRemaining = rowDimension * colDimension
        self.minesRemaining = totalMines
        self.totalMines = totalMines
        initialMineProbability = totalMines/(rowDimension * colDimension)
        self.cells = []
        for i in range(rowDimension):
            row = []
            for j in range(colDimension):
                xPosBeg = i - 1 if i - 1 >= 0 else i
                xPosEnd = i + 1 if i + 1 <= rowDimension - 1 else i
                yPosBeg = j - 1 if j - 1 >= 0 else j
                yPosEnd = j + 1 if j + 1 <= colDimension - 1 else j
                temp_list = []
                for x in range(xPosBeg, xPosEnd + 1):
                    for y in range(yPosBeg, yPosEnd + 1):
                        temp_list.append((x, y))
                cell = Cell(CellState.COVERED, None,
                            initialMineProbability, i, j, temp_list)
                row.append(cell)
            self.cells.append(row)
        self.exploredCells = []
        self.uncoveredCells = []
        self.safequeue = collections.deque()
        self.minequeue = collections.deque()
        self.lastX = startX
        self.lastY = startY
        self.cellsCopy = []
        self.bt_solution = []
        self.bactrackOverAllOrOnlyBoundary = False

    def isAdjCellUncovered(self, xPos, yPos):
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= self.rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= self.colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if self.cells[i][j].cell_state == CellState.UNCOVERED:
                    return True
        return False

    def get_adj_cells(self, cells, xPos, yPos):
        ''' returns the list of adjacent covered and flagged cells
            as a list of Cell class objects'''

        adj_c_cells = []
        adj_f_cells = []
        adj_u_cells = []
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= self.rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= self.colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if cells[i][j].cell_state == CellState.COVERED:
                    adj_c_cells.append((i,j))
                if cells[i][j].cell_state == CellState.FLAGGED:
                    adj_f_cells.append((i,j))
                if cells[i][j].cell_state == CellState.UNCOVERED:
                    if i == xPos and j == yPos:
                        continue
                    else:
                        adj_u_cells.append((i, j))
        return (adj_c_cells, adj_f_cells, adj_u_cells)

    def decideActionByProbability(self):
        minProb = 1.1
        for i in range(self.rowDimension):
            for j in range(self.colDimension):
                if self.cells[i][j].cell_state != CellState.UNCOVERED and self.cells[i][j].cell_state != CellState.FLAGGED:
                    mineProbabilty = self.cells[i][j].mine_probability
                    if mineProbabilty < minProb:
                        minProb = mineProbabilty
                        self.lastX = i
                        self.lastY = j
        return Action(AI.Action.UNCOVER, self.lastY, self.lastX)

    def getMineProbability(self, mines, cells):
        ''' mines --> No of mines in adjacent covered cells
            cells --> No of adjacent covered cells '''
        if cells > 0:
            return mines/cells

    def getBoundaryCells(self):
        '''Gets boundary Cells and all Covered cells'''
        boundaryList = []
        coveredList = []
        for cellRow in self.cells:
            for cell in cellRow:
                if self.cells[cell.xPos][cell.yPos].cell_state != CellState.COVERED:
                    continue
                coveredList.append((cell.xPos, cell.yPos))
                if self.isAdjCellUncovered(cell.xPos, cell.yPos):
                    boundaryList.append((cell.xPos, cell.yPos))
        return boundaryList, coveredList

    def getIsolatedBoundarys(self, boundaryList):
        '''Gets isolated boundary areas'''
        # sorted(boundaryList, key=lambda element: (element[0], element[1]))
        regions = []
        visited = []
        while True:
            q = queue.Queue()
            region = []
            for b in boundaryList:
                if b not in visited:
                    q.put(b)
                    break
            if q.empty():
                break
            while not q.empty():
                bl = q.get()
                region.append(bl)
                visited.append(bl)
                for c in boundaryList:
                    isConnected = False
                    if c not in region:
                        if c in self.cells[bl[0]][bl[1]].adjCells:
                            isConnected = True
                            break
                if isConnected and c not in q.queue:
                    q.put(c)
            regions.append(region)
        return regions

    def getSmallestIsolatedBoundary(self, regions):
        '''Get sorted isolated boundary region by size'''
        minLen = 481
        minReg = []
        for region in regions:
            l = len(region)
            if l < minLen:
                minLen = l
                minReg = region
        return minReg

    def backtrackingAlgorithm(self, borderCells, position):
        '''Take the smallest possible area that can be considered in isolation
          Make a guess and keep moving forward until you reach a contradiction
          If you reach a contradiction then eliminate that assumption and try another
          till you reach a case that solves without contradiction'''
        flagCount = 0
        for cellRow in self.cellsCopy:
            for cell in cellRow:
                if cell.isMine == True:
                    flagCount = flagCount + 1
                if cell.cell_state == CellState.UNCOVERED:
                    adjCoveredCells, adjFlaggedCells, adjUncoveredCells = self.get_adj_cells(self.cellsCopy,
                                                                                             cell.xPos, cell.yPos)
                    if len(adjFlaggedCells) > cell.percept:
                        return
                    if len(cell.adjCells) - cell.percept < len(adjCoveredCells):
                        return
        if flagCount > self.totalMines:
            return
        if position == len(borderCells):
            if not self.backtrackOverAllOrOnlyBoundary and (flagCount < self.totalMines):
                return
            sol = []
            for b in borderCells:
                sol.append(self.cellsCopy[b[0]][b[1]].isMine)
                # bc = copy.deepcopy(self.cellsCopy[b[0]][b[1]])
                # if bc.cell_state == CellState.COVERED and (bc.isMine or bc.isSafe):
            self.backtrackingSolution.append(sol)
            # self.backtrackingSolution.append(bc)
            return
        bl = borderCells[position]
        # if len(self.backtrackingSolution) == 0:
        self.cellsCopy[bl[0]][bl[1]].isMine = True
        self.backtrackingAlgorithm(borderCells, position+1)
        self.cellsCopy[bl[0]][bl[1]].isMine = False

    def solveInPairs(self):
        #print("ENTERS")
        #bound = self.getBoundaryCells()
        #for x,y in bound:
        #    u_cells = self.get_adj_cells(self.cells, x, y)[2]
        #    bound_n_cells = list(set(u_cells) & set(bound))
        #    for n_x,n_y in bound_n_cells:
        #        cell_x = -100
        #        cell_y = -100
        #        diff = (n_x - x) + (n_y - y)
        #        p_diff = self.cells[n_x][n_y].percept - self.cells[x][y].percept
        #        if abs(p_diff) != 1:
        #            continue
        #        if n_x == x:
        #            cell_y = n_y - 1 if p_diff > 0 else y + 1
        #            diag_cells = [(x+1, cell_y), (x-1, cell_y)]
        #        elif n_y == y:
        #            cell_x = n_x - 1 if p_diff > 0 else x + 1
        #            diag_cells = [(cell_x, y+1), (cell_x, y-1)]
        #        n_c_cells = self.get_adj_cells(self.cells, n_x, n_y)[0]
        #        int_list = list(set(diag_cells) & set(n_c_cells))
        #        if len(int_list) == 1:
        #            self.minequeue.append((int_list[0][0],int_list[0][0]))
        #print(len(self.minequeue))

        for x,y in self.uncoveredCells:
            if self.cells[x][y].percept == 1:
                c_cells, f_cells, u_cells = self.get_adj_cells(self.cells, x, y)
                for i,j in u_cells:
                    count = 0
                    pos = -1
                    if i == x and self.cells[i][j].percept == 2:
                        diag_cells = [(x,j+1), (x,j-1)]
                        if (j+1 < self.colDimension) and (self.cells[diag_cells[0][0]][diag_cells[0][1]].cell_state == CellState.UNCOVERED):
                            count += 1
                            pos = 0
                        if j-1 > -1 and self.cells[diag_cells[1][0]][diag_cells[1][1]].cell_state == CellState.UNCOVERED:
                            count += 1
                            pos = 1
                        if count == 2:
                            continue
                        elif count == 1:
                            return Action(AI.Action.FLAG, diag_cells[pos][1], diag_cells[pos][0])
                    elif j == y and self.cells[i][j].percept == 2:
                        diag_cells = [(i+1,y), (i-1,y)]
                        if i+1 < self.rowDimension and  self.cells[diag_cells[0][0]][diag_cells[0][1]].cell_state == CellState.UNCOVERED:
                            count += 1
                            pos = 0
                        if i-1 > -1 and self.cells[diag_cells[1][0]][diag_cells[1][1]].cell_state == CellState.UNCOVERED:
                            count += 1
                            pos = 1
                        if count == 2:
                            continue
                        elif count == 1:
                            return Action(AI.Action.FLAG, diag_cells[pos][1], diag_cells[pos][0])

        #changed = False
        # For each open cell (x,y)
        #for cellRow in self.cells:
        #    for cell in cellRow:
        #        if cell.cell_state == CellState.UNCOVERED:
        #for i,j in self.uncoveredCells:
        #    cell = self.cells[i][j]
        #    percept = cell.percept
        #    adjCovered, adjFlagged, adjUncovered = self.get_adj_cells(self.cells,
        #                                                              cell.xPos, cell.yPos)
        #    if len(adjCovered) == 0:
        #        continue
        #    percept = percept - len(adjFlagged)
        #    # for each neighbour which is open
        #    for x, y in adjUncovered:
        #        if x == cell.xPos or y == cell.yPos:
        #            adjPercept = self.cells[x][y].percept
        #            # get neighbours to adj cell
        #            nAdjCovered, nAdjFlagged, nAdjUncovered = self.get_adj_cells(self.cells,
        #                                                                          x, y)
        #            adjPercept = adjPercept - len(nAdjFlagged)
        #            # check if each unopened neighbour of first cell is a neighbour of 2nd cell
        #            for c in adjCovered:
        #                if c not in nAdjCovered:
        #                    break
        #            # Open all cells unique to the neighbour
        #            if adjPercept == percept:
        #                for uc in nAdjCovered:
        #                    if uc not in adjCovered:
        #                        self.cells[uc[0]][uc[1]].isSafe = True
        #                        #self.safeCells.append(uc)
        #                        changed = True
        #                        self.lastX = uc[0]
        #                        self.lastY = uc[1]
        #                        return Action(AI.Action.UNCOVER, uc[1], uc[0])
        #            # elif adjPercept - percept == len(nAdjFlagged) - len(adjFlagged):
        #            #     # Flag all cells unique to 2nd cell
        #            #     for uc in nAdjCovered:
        #            #         if uc not in adjCovered:
        #            #             self.cells[uc[0]][uc[1]].isMine = True
        #            #             self.minesRemaining = self.minesRemaining - 1
        #            #             changed = True
        #            #             self.lastX = uc[0]
        #            #             self.lastY = uc[1]
        #            #             return Action(AI.Action.FLAG, uc[1], uc[0])
        #return None

    def getAction(self, number: int) -> "Action Object":

        self.cells[self.lastX][self.lastY].percept = number
        if number == -1:
            self.cells[self.lastX][self.lastY].cell_state = CellState.FLAGGED
        else:
            self.cells[self.lastX][self.lastY].cell_state = CellState.UNCOVERED
            self.uncoveredCells.append((self.lastX,self.lastY))

        if (self.lastX,self.lastY) not in self.exploredCells:
            self.exploredCells.append((self.lastX,self.lastY))

        adjCells, adjFlaggedCells, uc_cells = self.get_adj_cells(self.cells, self.lastX, self.lastY)
        adjCellsNum = len(adjCells)
        adjFlaggedCellsNum = len(adjFlaggedCells)
        cellMineProb = 1 if number == -1 else self.getMineProbability(number, adjCellsNum)

        for xPos,yPos in adjCells:
            self.cells[xPos][yPos].mine_probability = cellMineProb
            if (xPos,yPos) not in self.exploredCells:
                self.exploredCells.append((xPos,yPos))
            if number == 0 or number == adjFlaggedCellsNum:
                if not self.cells[xPos][yPos].isSafe:
                    self.cells[xPos][yPos].isSafe = True
                    self.safequeue.append((xPos, yPos))
            elif number - adjFlaggedCellsNum == adjCellsNum:
                if not self.cells[xPos][yPos].isMine:
                    self.cells[xPos][yPos].isMine = True
                    self.minequeue.append((xPos,yPos))
                    self.minesRemaining = self.minesRemaining - 1

        for x,y in self.uncoveredCells:
            cellAdjCoveredCells, cellAdjFlagged, uc_cells = self.get_adj_cells(self.cells, x, y)
            cellAdjFlaggedNum = len(cellAdjFlagged)
            cellAdjCoveredCellsNum = len(cellAdjCoveredCells)
            if self.cells[x][y].percept - cellAdjFlaggedNum == cellAdjCoveredCellsNum:
                for xPos,yPos in cellAdjCoveredCells:
                    if not self.cells[xPos][yPos].isMine:
                        self.cells[xPos][yPos].isMine = True
                        self.minequeue.append((xPos,yPos))
                        self.minesRemaining = self.minesRemaining - 1
            if self.cells[x][y].percept == cellAdjFlaggedNum:
                for xPos,yPos in cellAdjCoveredCells:
                    if not self.cells[xPos][yPos].isSafe:
                        self.cells[xPos][yPos].isSafe = True
                        self.safequeue.append((xPos,yPos))

        while(self.safequeue):
            x,y = self.safequeue.pop()
            if self.cells[x][y].cell_state == CellState.COVERED:
                self.lastX = x
                self.lastY = y
                return Action(AI.Action.UNCOVER, y, x)
        while(self.minequeue):
            x,y = self.minequeue.pop()
            if self.cells[x][y].cell_state == CellState.COVERED:
                self.lastX = x
                self.lastY = y
                return Action(AI.Action.FLAG, y, x)

        action = self.solveInPairs()
        if action:
            return action

        boundaryList, coveredList = self.getBoundaryCells()
        self.backtrackOverAllOrOnlyBoundary = False
        if len(coveredList) - len(boundaryList) > 8:
            self.backtrackOverAllOrOnlyBoundary = True
        else:
            boundaryList = coveredList
        if len(boundaryList) > 0:
            isolatedBoundarys = self.getIsolatedBoundarys(boundaryList)
            isolatedBoundarys.sort(key=len)
            solutionFound = False
            while not solutionFound:
                for smallestIsolatedBoundary in isolatedBoundarys:
                    if len(smallestIsolatedBoundary) < 13:
                        self.cellsCopy = copy.deepcopy(self.cells)
                        self.backtrackingSolution = []
                        self.backtrackingAlgorithm(smallestIsolatedBoundary, 0)
                        if self.backtrackingSolution and len(self.backtrackingSolution) > 0:
                            for i in range(0, len(smallestIsolatedBoundary)):
                                isMine = True
                                isSafe = True
                                for sol in self.backtrackingSolution:
                                    if not sol[i]:
                                        isMine = False
                                    if sol[i]:
                                        isSafe = False
                                b = smallestIsolatedBoundary[i]
                                if isMine:
                                    self.cells[b[0]][b[1]].isMine = True
                                    self.minesRemaining = self.minesRemaining - 1
                                    self.lastX = b[0]
                                    self.lastY = b[1]
                                    solutionFound = True
                                    return Action(AI.Action.FLAG, b[1], b[0])
                                elif isSafe:
                                    self.cells[b[0]][b[1]].isSafe = True
                                    self.safeCells.append((b[0], b[1]))
                                    self.lastX = b[0]
                                    self.lastY = b[1]
                                    solutionFound = True
                                    return Action(AI.Action.UNCOVER, b[1], b[0])
                    else:
                        solutionFound = True
                        break
                solutionFound = True
                break

        if self.cellsRemaining > len(self.exploredCells) and self.minesRemaining > number:
            currMinePercept = 0 if number == -1 else number
            mineProbRemaining = self.getMineProbability(
                self.minesRemaining - currMinePercept, self.cellsRemaining - len(self.exploredCells))
            for xPos in range(self.rowDimension):
                for yPos in range(self.colDimension):
                    if (xPos,yPos) not in self.exploredCells and (xPos,yPos) not in adjCells and (xPos,yPos) not in adjFlaggedCells:
                        self.cells[xPos][yPos].mine_probability = mineProbRemaining
        return self.decideActionByProbability()
