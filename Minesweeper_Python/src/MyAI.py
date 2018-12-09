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
import queue
import copy
count = 0

class Cell:
    def __init__(self, cell_state, percept, mine_probability, xPos, yPos):
        self.cell_state = cell_state
        self.percept = percept
        self.mine_probability = mine_probability
        self.xPos = xPos
        self.yPos = yPos
        self.isSafe = False
        self.isMine = False
        self.adjCells = []


class CellState(Enum):
    COVERED = 0
    UNCOVERED = 1
    FLAGGED = 2
    UNFLAGGED = 3


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startY, startX):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.cellsRemaining = rowDimension * colDimension
        self.minesRemaining = totalMines
        initialMineProbability = totalMines/(rowDimension * colDimension)
        self.cells = []
        for i in range(rowDimension):
            row = []
            for j in range(colDimension):
                cell = Cell(CellState.COVERED, None,
                            initialMineProbability, i, j)
                xPosBeg = i - 1 if i - 1 >= 0 else i
                xPosEnd = i + 1 if i + 1 <= rowDimension - 1 else i
                yPosBeg = j - 1 if j - 1 >= 0 else j
                yPosEnd = j + 1 if j + 1 <= colDimension - 1 else j
                for x in range(xPosBeg, xPosEnd + 1):
                    for y in range(yPosBeg, yPosEnd + 1):
                        cell.adjCells.append((x, y))
                row.append(cell)
            self.cells.append(row)
        self.exploredCells = []
        self.safeCells = []
        self.lastX = startX
        self.lastY = startY
        self.cellsCopy = []
        self.backtrackingSolution = []
        self.backtrackOverAllOrOnlyBoundary = False

    def isAdjCellUncovered(self, xPos, yPos, rowDimension, colDimension):
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if self.cells[i][j].cell_state == CellState.UNCOVERED:
                    return True
        return False

    def get_adj_cells(self, cells, xPos, yPos, rowDimension, colDimension):
        ''' returns the list of adjacent covered and flagged cells
            as a list of Cell class objects'''
        adj_c_cells = []
        adj_f_cells = []
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if cells[i][j].cell_state == CellState.COVERED:
                    adj_c_cells.append((i, j))
                if cells[i][j].cell_state == CellState.FLAGGED:
                    adj_f_cells.append((i, j))
        return (adj_c_cells, adj_f_cells)

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
                if self.isAdjCellUncovered(cell.xPos, cell.yPos, self.rowDimension, self.colDimension):
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

    # def getSmallestIsolatedBoundary(self, regions):
    #     '''Get smallest isolated boundary region'''
    #     minLen = 481
    #     minReg = []
    #     for region in regions:
    #         l = len(region)
    #         if l < minLen:
    #             minLen = l
    #             minReg = region
    #     return minReg

    def backtrackingAlgorithm(self, borderCells, position):
        '''Take the smallest possible area that can be considered in isolation
          Make a guess and keep moving forward until you reach a contradiction
          If you reach a contradiction then eliminate that assumption and try another
          till you reach a case that solves without contradiction'''
        global count
        #count += 1
        #print(count)
        flagCount = 0
        for cellRow in self.cellsCopy:
            for cell in cellRow:
                if cell.isMine == True:
                    flagCount = flagCount + 1
                if cell.cell_state == CellState.UNCOVERED:
                    adjCoveredCells, adjFlaggedCells = self.get_adj_cells(self.cellsCopy,
                                                                          cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    if len(adjFlaggedCells) > cell.percept:
                        return
                    if len(cell.adjCells) - cell.percept < len(adjCoveredCells):
                        return
        if flagCount > self.totalMines:
            return
        if position == len(borderCells):
            if not self.backtrackOverAllOrOnlyBoundary and (flagCount < self.totalMines):
                return
            for b in borderCells:
                if self.cellsCopy[b[0]][b[1]].cell_state == CellState.COVERED and (self.cellsCopy[b[0]][b[1]].isMine or self.cellsCopy[b[0]][b[1]].isSafe):
                    self.backtrackingSolution.append(b)
            return
        bl = borderCells[position]
        self.cellsCopy[bl[0]][bl[1]].isMine = True
        self.backtrackingAlgorithm(borderCells, position+1)
        self.cellsCopy[bl[0]][bl[1]].isMine = False
        self.cellsCopy[bl[0]][bl[1]].isSafe = True
        self.backtrackingAlgorithm(borderCells, position + 1)
        self.cellsCopy[bl[0]][bl[1]].isSafe = False

    def getAction(self, number: int) -> "Action Object":
        self.cells[self.lastX][self.lastY].percept = number
        if number == -1:
            self.cells[self.lastX][self.lastY].cell_state = CellState.FLAGGED
        else:
            self.cells[self.lastX][self.lastY].cell_state = CellState.UNCOVERED

        if (self.lastX, self.lastY) not in self.exploredCells:
            self.exploredCells.append((self.lastX, self.lastY))

        adjCells, adjFlaggedCells = self.get_adj_cells(self.cells,
                                                       self.lastX, self.lastY, self.rowDimension, self.colDimension)
        adjCellsNum = len(adjCells)
        adjFlaggedCellsNum = len(adjFlaggedCells)
        cellMineProb = 1 if number == - \
            1 else self.getMineProbability(number, adjCellsNum)

        for xPos, yPos in adjCells:
            self.cells[xPos][yPos].mine_probability = cellMineProb
            if (xPos, yPos) not in self.exploredCells:
                self.exploredCells.append((xPos, yPos))
            if number == 0 or number == adjFlaggedCellsNum:
                if (xPos, yPos) not in self.safeCells:
                    self.cells[xPos][yPos].isSafe = True
                    self.safeCells.append((xPos, yPos))
            elif number - adjFlaggedCellsNum == adjCellsNum:
                if not self.cells[xPos][yPos].isMine:
                    self.cells[xPos][yPos].isMine = True
                    self.minesRemaining = self.minesRemaining - 1

        if self.safeCells and len(self.safeCells):
            for (xPos, yPos) in self.safeCells:
                if self.cells[xPos][yPos].cell_state == CellState.COVERED:
                    self.lastX = xPos
                    self.lastY = yPos
                    return Action(AI.Action.UNCOVER, yPos, xPos)

        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.UNCOVERED and cell.percept > 0:
                    cellAdjCoveredCells, cellAdjFlagged = self.get_adj_cells(self.cells,
                                                                             cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    cellAdjFlaggedNum = len(cellAdjFlagged)
                    cellAdjCoveredCellsNum = len(cellAdjCoveredCells)
                    if cell.percept - cellAdjFlaggedNum == cellAdjCoveredCellsNum:
                        for xPos, yPos in cellAdjCoveredCells:
                            if not self.cells[xPos][yPos].isMine:
                                self.cells[xPos][yPos].isMine = True
                                self.minesRemaining = self.minesRemaining - 1
        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.COVERED and cell.isMine:
                    self.lastX = cell.xPos
                    self.lastY = cell.yPos
                    return Action(AI.Action.FLAG, cell.yPos, cell.xPos)

        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.UNCOVERED and cell.percept > 0:
                    cellAdjCoveredCells, cellAdjFlagged = self.get_adj_cells(self.cells,
                                                                             cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    cellAdjFlaggedNum = len(cellAdjFlagged)
                    cellAdjCoveredCellsNum = len(cellAdjCoveredCells)
                    if cell.percept == cellAdjFlaggedNum:
                        for xPos, yPos in cellAdjCoveredCells:
                            if (xPos, yPos) not in self.safeCells:
                                self.cells[xPos][yPos].isSafe = True
                                self.safeCells.append(
                                    (xPos, yPos))
        if self.safeCells and len(self.safeCells) > 0:
            for xPos, yPos in self.safeCells:
                if self.cells[xPos][yPos].cell_state == CellState.COVERED:
                    self.lastX = xPos
                    self.lastY = yPos
                    return Action(AI.Action.UNCOVER, yPos, xPos)

        boundaryList, coveredList = self.getBoundaryCells()
        self.backtrackOverAllOrOnlyBoundary = False
        if len(coveredList) - len(boundaryList) > 8:
            self.backtrackOverAllOrOnlyBoundary = True
        else:
            boundaryList = coveredList
        if len(boundaryList) > 0:
            isolatedBoundarys = self.getIsolatedBoundarys(boundaryList)
            isolatedBoundarys.sort(key=len)
            #new_isolated_boundarys = []
            #for boundary_list in isolatedBoundarys:
            #    new_list = []
            #    if len(boundary_list) > 10:
            #        new_list.append(boundary_list[0:10])
            #        new_list.append(boundary_list[10:len(boundary_list)])
            #        new_isolated_boundarys.append(new_list[0])
            #        new_isolated_boundarys.append(new_list[1])
            #    else:
            #        new_isolated_boundarys.append(boundary_list)
            ##for it in new_isolated_boundarys:
            ##    print(len(it))
            ##import sys
            ##sys.exit()
            for smallestIsolatedBoundary in isolatedBoundarys:
                if len(smallestIsolatedBoundary) > 8:
                    continue
                self.cellsCopy = copy.deepcopy(self.cells)
                self.backtrackingSolution = []
                self.backtrackingAlgorithm(smallestIsolatedBoundary, 0)
                count = 0
                if self.backtrackingSolution and len(self.backtrackingSolution) > 0:
                    for b in self.backtrackingSolution:
                        if self.cellsCopy[b[0]][b[1]].cell_state == CellState.COVERED:
                            if self.cellsCopy[b[0]][b[1]].isMine:
                                self.cells[b[0]][b[1]].isMine = True
                                return Action(AI.Action.FLAG, b[1], b[0])
                            elif self.cellsCopy[b[0]][b[1]].isSafe:
                                self.cells[b[0]][b[1]].isSafe = True
                                self.safeCells.append((b[0], b[1]))
                                return Action(AI.Action.UNCOVER, b[1], b[0])

        if self.cellsRemaining > len(self.exploredCells) and self.minesRemaining > number:
            currMinePercept = 0 if number == -1 else number
            mineProbRemaining = self.getMineProbability(
                self.minesRemaining - currMinePercept, self.cellsRemaining - len(self.exploredCells))
            for xPos in range(self.rowDimension):
                for yPos in range(self.colDimension):
                    if (xPos, yPos) not in self.exploredCells and (xPos, yPos) not in adjCells and (xPos, yPos) not in adjFlaggedCells:
                        cell.mine_probability = mineProbRemaining
                        self.cells[xPos][yPos].mine_probability = mineProbRemaining
        return self.decideActionByProbability()
