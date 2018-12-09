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

class Cell:
    def __init__(self, cell_state, percept, mine_probability, xPos, yPos):
        self.cell_state = cell_state
        self.percept = percept
        self.mine_probability = mine_probability
        self.xPos = xPos
        self.yPos = yPos
        self.isSafe = False
        self.isMine = False

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
        initialMineProbability = totalMines/(rowDimension * colDimension)
        self.cells = []
        for i in range(rowDimension):
            row = []
            for j in range(colDimension):
                cell = Cell(CellState.COVERED, None,
                            initialMineProbability, i, j)
                row.append(cell)
            self.cells.append(row)
        self.exploredCells = []
        self.uncoveredCells = []
        self.safequeue = collections.deque()
        self.minequeue = collections.deque()
        self.lastX = startX
        self.lastY = startY

    def get_adj_cells(self, xPos, yPos):
        ''' returns the list of adjacent covered and flagged cells
            as a list of Cell class objects'''

        adj_c_cells = []
        adj_f_cells = []
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= self.rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= self.colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if self.cells[i][j].cell_state == CellState.COVERED:
                    adj_c_cells.append((i,j))
                if self.cells[i][j].cell_state == CellState.FLAGGED:
                    adj_f_cells.append((i,j))
        return (adj_c_cells, adj_f_cells)

    def decideAction(self):
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

    def getAction(self, number: int) -> "Action Object":

        self.cells[self.lastX][self.lastY].percept = number
        if number == -1:
            self.cells[self.lastX][self.lastY].cell_state = CellState.FLAGGED
        else:
            self.cells[self.lastX][self.lastY].cell_state = CellState.UNCOVERED
            self.uncoveredCells.append((self.lastX,self.lastY))

        if (self.lastX,self.lastY) not in self.exploredCells:
            self.exploredCells.append((self.lastX,self.lastY))

        adjCells, adjFlaggedCells = self.get_adj_cells(self.lastX, self.lastY)
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
            cellAdjCoveredCells, cellAdjFlagged = self.get_adj_cells(x, y)
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

        if self.cellsRemaining > len(self.exploredCells) and self.minesRemaining > number:
            currMinePercept = 0 if number == -1 else number
            mineProbRemaining = self.getMineProbability(
                self.minesRemaining - currMinePercept, self.cellsRemaining - len(self.exploredCells))
            for xPos in range(self.rowDimension):
                for yPos in range(self.colDimension):
                    if (xPos,yPos) not in self.exploredCells and (xPos,yPos) not in adjCells and (xPos,yPos) not in adjFlaggedCells:
                        self.cells[xPos][yPos].mine_probability = mineProbRemaining
        return self.decideAction()
