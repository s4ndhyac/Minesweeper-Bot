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
import sys
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
                cell = Cell(CellState.COVERED, None,
                            initialMineProbability, i, j)
                row.append(cell)
            self.cells.append(row)
        self.exploredCells = []
        self.lastX = startX
        self.lastY = startY

    def get_Ccells(self, xPos, yPos, rowDimension, colDimension):
        ''' 
        returns the covered adjacent cells as a list of Cell class objects
        '''
        adjCells = []
        xPosBeg = xPos - 1 if xPos - 1 >= 0 else xPos
        xPosEnd = xPos + 1 if xPos + 1 <= rowDimension - 1 else xPos
        yPosBeg = yPos - 1 if yPos - 1 >= 0 else yPos
        yPosEnd = yPos + 1 if yPos + 1 <= colDimension - 1 else yPos
        for i in range(xPosBeg, xPosEnd + 1):
            for j in range(yPosBeg, yPosEnd + 1):
                if self.cells[i][j].cell_state != CellState.UNCOVERED:
                    adjCells.append(self.cells[i][j])
        return adjCells

    def decideAction(self):
        minProb = 1.1
        for i in range(self.rowDimension):
            for j in range(self.colDimension):
                if self.cells[i][j].cell_state != CellState.UNCOVERED:
                    mineProbabilty = self.cells[i][j].mine_probability
                    if mineProbabilty < minProb:
                        minProb = mineProbabilty
                        self.lastX = i
                        self.lastY = j
        return Action(AI.Action.UNCOVER, self.lastX, self.lastY)

    def getMineProbability(self, mines, cells):
        ''' 
        mines --> No of mines in Adjacent and covered cells
        cells --> adjacent and covered cells
        returns the mine probability
        '''
        if cells > 0:
            return mines/cells

    def getAction(self, number: int) -> "Action Object":
        #self.cells[self.lastX][self.lastY].percept = number
        self.cells[self.lastX][self.lastY].cell_state = CellState.UNCOVERED

        if self.cells[self.lastX][self.lastY] not in self.exploredCells:
            self.exploredCells.append(self.cells[self.lastX][self.lastY])
        adjCells = self.get_Ccells(
            self.lastX, self.lastY, self.rowDimension, self.colDimension)
        cellMineProb = self.getMineProbability(number, len(adjCells))

        for cell in adjCells:
            self.cells[cell.xPos][cell.yPos].mine_probability = cellMineProb
            if self.cells[cell.xPos][cell.yPos] not in self.exploredCells:
                self.exploredCells.append(self.cells[cell.xPos][cell.yPos])

        if self.cellsRemaining > len(self.exploredCells):
            mineProbRemaining = self.getMineProbability(
                self.minesRemaining - number, self.cellsRemaining - len(self.exploredCells))
            for cellRow in self.cells:
                for cell in cellRow:
                    if cell not in self.exploredCells and cell not in adjCells:
                        self.cells[cell.xPos][cell.yPos].mine_probability = mineProbRemaining
        return self.decideAction()
