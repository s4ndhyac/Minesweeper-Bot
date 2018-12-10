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
from itertools import combinations


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

    def get_adj_cells(self, cells, xPos, yPos, rowDimension, colDimension):
        ''' returns the list of adjacent covered and flagged cells
            as a list of Cell class objects'''
        adj_c_cells = []
        adj_f_cells = []
        adj_u_cells = []
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

    def trivial(self, cells):
        to_flag = set()
        to_open = set()
        for cellRow in cells:
            for cell in cellRow:
                if cell.cell_state == CellState.UNCOVERED and cell.percept > 0:
                    adjCovered, adjFlagged, adjUncovered = self.get_adj_cells(
                        cells, cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    if len(adjCovered) == cell.percept:
                        for c in cell.adjCells:
                            if cells[c[0]][c[1]].cell_state == CellState.COVERED:
                                to_flag.add(c)
                    elif len(adjFlagged) == cell.percept:
                        for c in cell.adjCells:
                            if cells[c[0]][c[1]].cell_state == CellState.COVERED:
                                to_open.add(c)
        return (to_flag, to_open)

    def getProspectiveCells(self, cell):
        r = []
        for cell in cell.adjCells:
            if self.cells[cell[0]][cell[1]].cell_state == CellState.COVERED:
                r.append(cell)
        return r

    def in_all(self, element, list_of_sets):
        for s in list_of_sets:
            if element not in s:
                return False
        else:
            return True

    # non-trivial AI, works by iteration over possible mine layout around the cell
    # if a trivial algorithm returns the same cell for every single permutation,
    #   it is added to output
    # return two sets: cells to flag and cells to open
    def nonTrivial(self, cell, cells):
        # sets to return
        ret_flags = set()
        ret_opens = set()
        # if cell is viable for permutation tests
        adjCovered, adjFlagged, adjUncovered = self.get_adj_cells(
            cells, cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
        if cell.cell_state == CellState.UNCOVERED and cell.percept - len(adjFlagged) > 0:
            grp = self.getProspectiveCells(cell)
            if grp:
                to_flags = []
                to_opens = []
                for combo in combinations(grp, cell.percept - len(adjFlagged)):
                    for acell in combo:
                        cells[acell[0]][acell[1]].percept = -1
                        cells[acell[0]][acell[1]].cell_state = CellState.FLAGGED
                    to_flag_i, to_open_i = self.trivial(cells)
                    for acell in combo:
                        cells[acell[0]][acell[1]].percept = None
                        cells[acell[0]][acell[1]].cell_state = CellState.COVERED
                    to_flags.append(to_flag_i)
                    to_opens.append(to_open_i)
            if to_flags:
                if to_flags[0]:
                    for element in to_flags[0]:
                        if self.in_all(element, to_flags):
                            ret_flags.add(element)
            if to_opens:
                if to_opens[0]:
                    for element in to_opens[0]:
                        if self.in_all(element, to_opens):
                            ret_opens.add(element)
        return (ret_flags, ret_opens)

    def solveInPairs(self):
        changed = False
        # For each open cell (x,y)
        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.UNCOVERED:
                    percept = cell.percept
                    adjCovered, adjFlagged, adjUncovered = self.get_adj_cells(self.cells,
                                                                              cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    if len(adjCovered) == 0:
                        continue
                    percept = percept - len(adjFlagged)
                    # for each neighbour which is open
                    for x, y in adjUncovered:
                        if x == cell.xPos or y == cell.yPos:
                            adjPercept = self.cells[x][y].percept
                            # get neighbours to adj cell
                            nAdjCovered, nAdjFlagged, nAdjUncovered = self.get_adj_cells(self.cells,
                                                                                         x, y, self.rowDimension, self.colDimension)
                            adjPercept = adjPercept - len(nAdjFlagged)
                            # check if each unopened neighbour of first cell is a neighbour of 2nd cell
                            for c in adjCovered:
                                if c not in nAdjCovered:
                                    break
                            # Open all cells unique to the neighbour
                            if adjPercept == percept:
                                for uc in nAdjCovered:
                                    if uc not in adjCovered:
                                        self.cells[uc[0]][uc[1]].isSafe = True
                                        self.safeCells.append(uc)
                                        changed = True
                                        self.lastX = uc[0]
                                        self.lastY = uc[1]
                                        return Action(AI.Action.UNCOVER, uc[1], uc[0])
        return None

    def getAction(self, number: int) -> "Action Object":
        self.cells[self.lastX][self.lastY].percept = number
        if number == -1:
            self.cells[self.lastX][self.lastY].cell_state = CellState.FLAGGED
        else:
            self.cells[self.lastX][self.lastY].cell_state = CellState.UNCOVERED

        if (self.lastX, self.lastY) not in self.exploredCells:
            self.exploredCells.append((self.lastX, self.lastY))

        adjCells, adjFlaggedCells, adfUncoveredCells = self.get_adj_cells(self.cells,
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
                    cellAdjCoveredCells, cellAdjFlagged, cellAdjUncovered = self.get_adj_cells(self.cells,
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
                    cellAdjCoveredCells, cellAdjFlagged, cellAdjUncovered = self.get_adj_cells(self.cells,
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

        if self.cellsRemaining == 480:
            action = self.solveInPairs()
            if action:
                return action
            to_flag, to_open = self.trivial(self.cells)
            for cellRow in self.cells:
                for cell in cellRow:
                    self.cellsCopy = copy.deepcopy(self.cells)
                    cell_flags, cell_opens = self.nonTrivial(
                        cell, self.cellsCopy)
                    to_flag = to_flag | cell_flags
                    to_open = to_open | cell_opens
                    if to_flag:
                        for c in to_flag:
                            self.cells[c[0]][c[1]].isMine = True
                            self.minesRemaining = self.minesRemaining - 1
                    if to_open:
                        for c in to_open:
                            self.cells[c[0]][c[1]].isSafe = True
                            self.safeCells.append((c[0], c[1]))
            if self.safeCells and len(self.safeCells) > 0:
                for xPos, yPos in self.safeCells:
                    if self.cells[xPos][yPos].cell_state == CellState.COVERED:
                        self.lastX = xPos
                        self.lastY = yPos
                        return Action(AI.Action.UNCOVER, yPos, xPos)
            for cellRow in self.cells:
                for cell in cellRow:
                    if cell.cell_state == CellState.COVERED and cell.isMine:
                        self.lastX = cell.xPos
                        self.lastY = cell.yPos
                        return Action(AI.Action.FLAG, cell.yPos, cell.xPos)

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
