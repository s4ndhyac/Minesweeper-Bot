# ==============================CS-199==================================
# FILE:			World.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the World class. This file sets up the
#				environment in which your agent exists and is responsible
#				for representing, maintaining, and changing the state of
#				the game.
#
# NOTES: 		- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import random
from ManualAI import ManualAI
from RandomAI import RandomAI
from MyAI import MyAI
from AI import AI


class World():

	# Tile class
	class __Tile():
		mine = False
		covered = True
		flag = False
		number = 0
		

	def __init__(self, filename=None, aiType="myai", verbose=False, debug=False):
		self.__verbose = verbose
		self.__debug = debug

		self.__colDimension = 0
		self.__rowDimension = 0
		self.__score = 0
		self.__board = None
		self.__totalMines = 0
		self.__flagsLeft = 0
		self.__coveredTiles = 0
		self.__movesMade = 0
		self.__movesLimit = 0

		self.__perceptNumber = 0
		self.__lastTile = None
		self.__lastAction = None

		try:
		# If file is provided, construct board based on file
			if filename != None:
				with open(filename, 'r') as file:
					self.__createBoard(file)
					firstMoveCoords = self.__getFirstMove(file)
					self.__addMines(file)
					self.__addNumbers()
					self.__coveredTiles = self.__colDimension * self.__rowDimension
					self.__flagsLeft = self.__totalMines
					self.__uncoverTile(firstMoveCoords[0], firstMoveCoords[1])
					self.__lastTile = (firstMoveCoords[0]+1, firstMoveCoords[1]+1)
					self.__lastAction = "UNCOVER"
					
		# If file not provided, construct board using defaults
			else:
				self.__createBoard()
				self.__addMines()
				self.__addNumbers()
				firstMoveCoords = self.__getFirstMove()
				self.__coveredTiles = self.__colDimension * self.__rowDimension
				self.__flagsLeft = self.__totalMines
				self.__uncoverTile(firstMoveCoords[0], firstMoveCoords[1])
				self.__lastTile = (firstMoveCoords[0]+1, firstMoveCoords[1]+1)
				self.__lastAction = "UNCOVER"

		except ValueError as e:
			print("Error: Cannot create board!")

		if aiType == "manual":
			self.__ai = ManualAI()
		elif aiType == "random":
			self.__ai = RandomAI(self.__rowDimension, self.__colDimension, self.__totalMines, firstMoveCoords[0], firstMoveCoords[1])
		elif aiType == "myai":
			self.__ai = MyAI(self.__rowDimension, self.__colDimension, self.__totalMines, firstMoveCoords[0], firstMoveCoords[1])

		if (self.__verbose and filename):
			print("Running on world: " + filename)


	def run(self) -> int:
		""" Engine of the game """
		while (True):
			if type(self.__ai) == ManualAI or self.__debug:
				self.__printWorld()
			if self.__movesMade > self.__movesLimit:
				break;

			try: 
				action = self.__ai.getAction(self.__perceptNumber)
				if self.__checkValidAction(action):
					if self.__doMove(action):
						break
			except ValueError:
				print("Error: Invalid action!")
			except IndexError:
				print("Error: Move is out of bounds!")

			if self.__debug and type(self.__ai) != ManualAI:
				input("Press ENTER to continue...")
		self.__handleGameover()
		self.__uncoverAll()
		if type(self.__ai) == ManualAI or self.__debug:
			self.__printWorld()

		if self.__score == (self.__colDimension * self.__rowDimension) - self.__totalMines:
			if self.__rowDimension == 8 and self.__colDimension == 8:
				return 1
			elif self.__rowDimension == 16 and self.__colDimension == 16:
				return 2
			elif self.__rowDimension == 16 and self.__colDimension == 30:
				return 3
			else:
				return 1
		else:
			return 0


	###############################################
	#				ACTIONS ON BOARD 			  #
	###############################################
	def __checkValidAction(self, actionObj: "Action Object") -> bool:
		""" Check if move is valid, and if coordinates are valid, returning a boolean """
		move = actionObj.getMove()
		X = actionObj.getX()
		Y = actionObj.getY()
		if move in [AI.Action.LEAVE, AI.Action.UNCOVER, AI.Action.FLAG, AI.Action.UNFLAG]:
			if self.__isInBounds(X, Y):
				return True
			raise IndexError
		raise ValueError


	def __doMove(self, actionObj: "Action Object") -> bool:
		""" Perform a move on the game board based on given action and x, y coords """
		""" Return True when game is over, False otherwise """
		self.__movesMade += 1

		move = actionObj.getMove()
		X = actionObj.getX()
		Y = actionObj.getY()
		self.__lastTile = (X+1, Y+1)
		if move == AI.Action.UNCOVER:
			self.__lastAction = "UNCOVER"
		elif move == AI.Action.FLAG:
			self.__lastAction = "FLAG"
		elif move == AI.Action.UNFLAG:
			self.__lastAction = "UNFLAG"
		elif move == AI.Action.LEAVE:
			self.__lastAction = "LEAVE"

		# LEAVE
		if move == AI.Action.LEAVE:
			if type(self.__ai) == ManualAI or self.__debug:
				print("Leaving game...")
			return True 							# Agent decides to leave game
		# UNCOVER
		elif move == AI.Action.UNCOVER:
			if self.__board[X][Y].mine:
				if type(self.__ai) == ManualAI or self.__debug:
					print("Gameover! Uncovered a mine! " + str(X+1), str(Y+1))
				return True 						# Agent uncovered a mine
			if type(self.__ai) == ManualAI:
				print("Uncovering: " + str(X+1) + ", " + str(Y+1))
			self.__uncoverTile(X, Y)
		# FLAG
		elif move == AI.Action.FLAG:
			if type(self.__ai) == ManualAI:
				print("Flagging: " + str(X+1) + ", " + str(Y+1))
			self.__flagTile(X, Y)
		# UNFLAG
		elif move == AI.Action.UNFLAG:
			if type(self.__ai) == ManualAI:
				print("Unflagging: " + str(X+1) + ", " + str(Y+1))
			self.__unflagTile(X, Y)
		return False 								# Game continues


	#####################################################
	#			SETTING UP THE GAME BOARD   			#
	#####################################################
	def __createBoard(self, inputStream: "filePointer" = None) -> None:
		""" Creates 2D tile array from first line of file and instantiates board instance variable """
		if inputStream:
			self.__rowDimension, self.__colDimension = [int(x) for x in inputStream.readline().split()]
			self.__board = [[self.__Tile() for i in range(self.__rowDimension)] for j in range(self.__colDimension)]
		else:
			self.__colDimension = 8		# Default sizes
			self.__rowDimension = 8		# Default size

			self.__board = [[self.__Tile() for i in range(self.__rowDimension)] for j in range(self.__colDimension)]
		
		self.__movesLimit = self.__colDimension * self.__rowDimension * 2


	def __getFirstMove(self, inputStream: "filePointer" = None) -> "tuple of ints": 
		""" Find the first move to be given to the agent, must be a "0" tile """
		if inputStream:
			startX, startY = [int(x)-1 for x in inputStream.readline().split()]
			if startX > self.__colDimension or startX < 0 or startY > self.__rowDimension or startY < 0:
				raise ValueError('First move coordinates are invalid')
		else:
			startX = self.__randomInt(self.__colDimension)
			startY = self.__randomInt(self.__rowDimension)
			while (self.__board[startX][startY].number != 0 or self.__board[startX][startY].mine):
				startX = self.__randomInt(self.__colDimension)
				startY = self.__randomInt(self.__rowDimension)
		return (startX, startY)


	def __addMines(self, inputStream: "filePointer" = None) -> None:
		""" Add mines to the game board""" 
		if inputStream:
			for r, line in zip(range(self.__rowDimension - 1, -1, -1), inputStream.readlines()):
				for c, tile in zip(range(self.__colDimension), line.split()):
					if tile == "1":
						self.__addMine(c, r)
		else:
			currentMines = 0
			while currentMines < 10:	# Default number of mines is 10
				r = self.__randomInt(self.__rowDimension)
				c = self.__randomInt(self.__colDimension)
				if not self.__board[c][r].mine:
					self.__addMine(c, r)
					currentMines += 1

					
	def __addMine(self, c: int, r: int) -> None:
		""" Add mine to tile located at (c, r) and update the Tile.mine attrbute """
		self.__board[c][r].mine = True
		self.__totalMines += 1		


	def __addNumbers(self) -> None:
		""" Iterate the board and add hint numbers for each mine """
		for r in range(self.__rowDimension):
			for c in range(self.__colDimension):
				if self.__board[c][r].mine:
					self.__addHintNumber(c, r+1)
					self.__addHintNumber(c, r-1)
					self.__addHintNumber(c+1, r)
					self.__addHintNumber(c-1, r)
					self.__addHintNumber(c-1, r+1)
					self.__addHintNumber(c+1, r+1)
					self.__addHintNumber(c-1, r-1)
					self.__addHintNumber(c+1, r-1)


	def __addHintNumber(self, c: int, r: int) -> None:
		""" Increment the hint number of a tile """
		if self.__isInBounds(c, r):
			self.__board[c][r].number += 1


	def __uncoverTile(self, c: int, r: int) -> None:
		""" Uncovers a tile """
		if self.__board[c][r].covered:
			self.__board[c][r].covered = False
			self.__coveredTiles -= 1
		self.__perceptNumber = self.__board[c][r].number


	def __uncoverAll(self) -> None:
		""" Uncovers all tiles """
		for r in range(self.__rowDimension):
			for c in range(self.__colDimension):
				self.__uncoverTile(c, r)
		self.__coveredTiles = 0


	def __flagTile(self, c: int, r: int) -> None:
		""" Flag a tile, coordinates adjusted to fix indexing """
		if self.__board[c][r].covered and not self.__board[c][r].flag and self.__flagsLeft > 0:
			self.__board[c][r].flag = True
			self.__flagsLeft -= 1
		if self.__flagsLeft < 0:
			self.__flagsLeft = 0
		self.__perceptNumber = -1


	def __unflagTile(self, c: int, r: int) -> None:
		""" Unflag a tile, coordinates adjusted to fix indexing """
		if self.__board[c][r].covered and self.__board[c][r].flag:
			self.__board[c][r].flag = False
			self.__flagsLeft += 1
		if self.__flagsLeft > 10:
			self.__flagsLeft = 10
		self.__perceptNumber = -1


	def __handleGameover(self) -> None:
		""" Check game board for completion after AI is done """
		for r in range(self.__rowDimension):
			for c in range(self.__colDimension):
				# If all safe tiles are uncovered
				if not self.__board[c][r].covered and not self.__board[c][r].mine:
					self.__score += 1


	#############################################
	#			 BOARD REPRESENTATION			#
	#############################################
	def __printWorld(self) -> None:
		""" Prints to console information about Minesweeper World """
		self.__printBoardInfo()
		self.__printActionInfo()
		self.__printAgentInfo()


	def __printBoardInfo(self) -> None:
		""" Print board for debugging """
		print("\nNumber of mines: " + str(self.__totalMines))
		print("Number of flags left: " + str(self.__flagsLeft))

		board_as_string = ""
		print("", end=" ")
		for r in range(self.__rowDimension - 1, -1, -1):
			print(str(r+1).ljust(2) + '|', end=" ")
			for c in range(self.__colDimension):
				self.__printTileInfo(c, r)
			if (r != 0):
				print('\n', end=" ")

		column_label = "     "
		column_border = "   "
		for c in range(1, self.__colDimension+1):
			column_border += "---"
			column_label += str(c).ljust(3)
		print(board_as_string)
		print(column_border)
		print(column_label)


	def __printAgentInfo(self) -> None:
		""" Prints information about the board that are useful to the user """
		print("Tiles covered: " + str(self.__coveredTiles) + " | Flags left: " + str(self.__flagsLeft) + " | Last action: {} on {}".format(self.__lastAction, self.__lastTile))


	def __printActionInfo(self) -> None:
		""" Prints available actions to the user if agent is ManualAI """
		if type(self.__ai) == ManualAI:
			print("Press \"L\" to leave game\nPress \"U\" to uncover a tile\nPress \"F\" to flag a tile\nPress \"N\" to unflag a tile: ")


	def __printTileInfo(self, c: int, r: int) -> None:
		""" Checks tile attributes and prints accordingly """
		if not self.__board[c][r].covered and self.__board[c][r].mine:
			print('B ', end=" ")
		elif not self.__board[c][r].covered:
			print(str(self.__board[c][r].number) + ' ', end=" ")
		elif self.__board[c][r].flag:
			print('? ', end=" ")
		elif self.__board[c][r].covered:
			print('. ', end=" ")
		

	#####################################################
	#		         HELPER FUNCTIONS					#
	#####################################################
	def __randomInt(self, limit: int) -> int:
		""" Return a random int within the range from 0 to limit """
		return random.randrange(limit)


	def __isInBounds(self, c: int, r: int) -> bool:
		""" Returns true if given coordinates are within the boundaries of the game board """
		if c < self.__colDimension and c >= 0 and r < self.__rowDimension and r >= 0:
			return True
		return False

