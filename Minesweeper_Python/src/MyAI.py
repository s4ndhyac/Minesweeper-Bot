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
from Cell import Cell
import CellState


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.cellsRemaining = rowDimension * colDimension
        self.minesRemaining = totalMines
        initialMineProbability = totalMines/(rowDimension * colDimension)
        self.cells = []
        for i in range(rowDimension):
            row = []
            for j in range(colDimension):
                cell = Cell(CellState.NOTUNCOVERED, None,
                            initialMineProbability, i, j)
                row.append(cell)
            self.cells.append(row)
        self.exploredCells = []
        self.safeCells = []
        self.lastX = startX
        self.lastY = startY

    def getAdjacentAndNotUncoveredCells(self, xPos, yPos, rowDimension, colDimension):
        adjCells = []
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if self.cells[i][j].cell_state == CellState.NOTUNCOVERED:
                    adjCells.append(self.cells[i][j])
        return adjCells

    def getAdjacentAndFlaggedCells(self, xPos, yPos, rowDimension, colDimension):
        adjCells = []
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if self.cells[i][j].cell_state == CellState.FLAGGED:
                    adjCells.append(self.cells[i][j])
        return adjCells

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
        return Action(AI.Action.UNCOVER, self.lastX, self.lastY)

    def getMineProbability(self, noOfMinesInAdjacentAndNotUncovered, adjacentAndNotUncoveredCells):
        return noOfMinesInAdjacentAndNotUncovered/adjacentAndNotUncoveredCells

    def getAction(self, number: int) -> "Action Object":
        self.cells[self.lastX][self.lastY].percept = number
        if number == -1:
            self.cells[self.lastX][self.lastY].cell_state = CellState.FLAGGED
        else:
            self.cells[self.lastX][self.lastY].cell_state = CellState.UNCOVERED
        if self.cells[self.lastX][self.lastY] not in self.exploredCells:
            self.exploredCells.append(self.cells[self.lastX][self.lastY])
        adjCells = self.getAdjacentAndNotUncoveredCells(
            self.lastX, self.lastY, self.rowDimension, self.colDimension)
        adjCellsNum = len(adjCells)
        adjFlaggedCells = self.getAdjacentAndFlaggedCells(
            self.lastX, self.lastX, self.rowDimension, self.colDimension)
        adjFlaggedCellsNum = len(adjFlaggedCells)
        for cell in adjCells:
            cellMineProb = 1 if number == - \
                1 else self.getMineProbability(number, adjCellsNum)
            cell.mine_probability = cellMineProb
            self.cells[cell.xPos][cell.yPos].mine_probability = cellMineProb
            if self.cells[cell.xPos][cell.yPos] not in self.exploredCells:
                self.exploredCells.append(self.cells[cell.xPos][cell.yPos])
            if number == 0:
                if self.cells[cell.xPos][cell.yPos] not in self.safeCells:
                    self.cells[cell.xPos][cell.yPos].isSafe = True
                    self.safeCells.append(self.cells[cell.xPos][cell.yPos])
            elif number - adjFlaggedCellsNum == adjCellsNum:
                if not self.cells[cell.xPos][cell.yPos].isMine:
                    self.cells[cell.xPos][cell.yPos].isMine = True
                    self.minesRemaining = self.minesRemaining - 1
            elif number == adjFlaggedCellsNum:
                if self.cells[cell.xPos][cell.yPos] not in self.safeCells:
                    self.cells[cell.xPos][cell.yPos].isSafe = True
                    self.safeCells.append(self.cells[cell.xPos][cell.yPos])
        if self.safeCells and len(self.safeCells) > 0:
            for cell in self.safeCells:
                if self.cells[cell.xPos][cell.yPos].cell_state == CellState.NOTUNCOVERED:
                    self.lastX = cell.xPos
                    self.lastY = cell.yPos
                    return Action(AI.Action.UNCOVER, cell.xPos, cell.yPos)
        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.UNCOVERED and cell.percept > 0:
                    cellAdjNotUncoveredCells = self.getAdjacentAndNotUncoveredCells(
                        cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    cellAdjFlagged = self.getAdjacentAndFlaggedCells(
                        cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    cellAdjFlaggedNum = len(cellAdjFlagged)
                    cellAdjNotUncoveredCellsNum = len(cellAdjNotUncoveredCells)
                    if cell.percept - cellAdjFlaggedNum == cellAdjNotUncoveredCellsNum:
                        for c in cellAdjNotUncoveredCells:
                            if not self.cells[c.xPos][c.yPos].isMine:
                                self.cells[c.xPos][c.yPos].isMine = True
                                self.minesRemaining = self.minesRemaining - 1
        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.NOTUNCOVERED and cell.isMine:
                    self.lastX = cell.xPos
                    self.lastY = cell.yPos
                    return Action(AI.Action.FLAG, cell.xPos, cell.yPos)
        for cellRow in self.cells:
            for cell in cellRow:
                if cell.cell_state == CellState.UNCOVERED and cell.percept > 0:
                    cellAdjNotUncoveredCells = self.getAdjacentAndNotUncoveredCells(
                        cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    cellAdjFlagged = self.getAdjacentAndFlaggedCells(
                        cell.xPos, cell.yPos, self.rowDimension, self.colDimension)
                    cellAdjFlaggedNum = len(cellAdjFlagged)
                    cellAdjNotUncoveredCellsNum = len(cellAdjNotUncoveredCells)
                    if cell.percept == cellAdjFlaggedNum:
                        for c in cellAdjNotUncoveredCells:
                            if self.cells[c.xPos][c.yPos] not in self.safeCells:
                                self.cells[c.xPos][c.yPos].isSafe = True
                                self.safeCells.append(
                                    self.cells[c.xPos][c.yPos])
        if self.safeCells and len(self.safeCells) > 0:
            for cell in self.safeCells:
                if self.cells[cell.xPos][cell.yPos].cell_state == CellState.NOTUNCOVERED:
                    self.lastX = cell.xPos
                    self.lastY = cell.yPos
                    return Action(AI.Action.UNCOVER, cell.xPos, cell.yPos)
        if self.cellsRemaining > len(self.exploredCells) and self.minesRemaining > number:
            currMinePercept = 0 if number == -1 else number
            mineProbRemaining = self.getMineProbability(
                self.minesRemaining - currMinePercept, self.cellsRemaining - len(self.exploredCells))
            for cellRow in self.cells:
                for cell in cellRow:
                    if cell not in self.exploredCells and cell not in adjCells and cell not in adjFlaggedCells:
                        cell.mine_probability = mineProbRemaining
                        self.cells[cell.xPos][cell.yPos].mine_probability = mineProbRemaining
        return self.decideAction()
