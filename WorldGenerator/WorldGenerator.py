# ==============================CS-199==================================
# FILE:			WorldGenerator.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file generates Worlds. The generator can be used to
#				create any number of worlds.
#
# NOTES: 		- "numWorlds" = number of world files to create
#				- "baseFileName" = the prefix of the file name, which
#								   is then followed by a number
#				- "rowDimension" = the number of rows
#				- "colDimension" = the number of columns
#				- "numMines" = the number of mines
#
#				- You can only generate worlds of the same dimensions
#				  and same number of mines. In order to generate worlds
#				  of other dimensions/ # of mines you have to run the
#				  generator again with different arguments.
#
#				- The minimum row and column dimension is 4.
#				- The minimum number of mines is 1.
#				
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import random
import os
import argparse


def generateWorlds(numWorlds: int, baseFileName: "string", rowDimension: int, colDimension: int, numMines: int) -> None:
	""" Generates N random worlds of a specified difficulty """
	""" Each generated world will be a text file with baseFileName followed by a number """
	for i in range(1, numWorlds+1):
		createWorldFile(baseFileName+str(i), rowDimension, colDimension, numMines)


def createWorldFile(filename: "string", rowDimension: int, colDimension: int, numMines: int) -> None:
	""" Create a single Minesweeper world file """
	print("Creating world " + filename + "...")
	dir_name = os.path.abspath("Problems")
	
	difficulty_name = filename.split("_", 1)[0]
	if os.path.isdir(os.path.join(dir_name, difficulty_name)):
	    directory_name = os.path.join(dir_name, difficulty_name)
	else:
	    directory_name = dir_name
	
	file_path = os.path.join(directory_name, filename+".txt")
	print(file_path)

	nRows = rowDimension
	nCols = colDimension
	nMines = numMines

	# Randomly set the starting tile
	startX = __randomInt(nCols+1)
	startY = __randomInt(nRows+1)
	startingPatch = [(startX, startY)]
	# Surrounding tiles can't have a mine
	for coord in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]:
		if __isInBounds(startX+coord[0], startY+coord[1], nRows, nCols):
			startingPatch.append((startX+coord[0], startY+coord[1]))
	
	# Randomly place mines that aren't in startingPatch
	mineCoords = []
	currentMines = 0
	while currentMines < nMines:
		x = __randomInt(nCols+1)
		y = __randomInt(nRows+1)
		if (x, y) not in startingPatch and (x, y) not in mineCoords:
			mineCoords.append((x, y))
			currentMines += 1

	# Open file for writing
	try:
		with open(file_path, 'w') as file:
			# Write dimensions
			file.write(str(nRows) + " " + str(nCols) + "\n")
			# Write starting square
			file.write(str(startX) + " " + str(startY) + "\n")
			# Write 2D grid
			for y in range(nRows, 0, -1):
				for x in range(1, nCols+1):
					if (x, y) in mineCoords:
						file.write("1 ")
					elif (x, y) in startingPatch:
						file.write("0 ")
					else:
						file.write("0 ")
				file.write("\n")
	except:
		print("ERROR: Failed to open file")


def __randomInt(limit: int) -> int:
	""" Return a random between 1 and limit """
	return random.randrange(1, limit)


def __isInBounds(x: int, y: int, nRows: int, nCols: int) -> bool:
	""" Check if x and y is within bounds """
	return (x >= 1 and x <= nCols and y >= 1 and y <= nRows)


def main():
	# Create parser
	parser = argparse.ArgumentParser(description="Process command line arugments for world generation")

	# Parse options																													# Help is default
	parser.add_argument("numFiles", help="Number of world files to create", action="store", type=int)								# Number of files
	parser.add_argument("filename", help="Base filename", action="store")															# Base filename
	parser.add_argument("rowDimension", help="Number of rows", action="store", type=int)
	parser.add_argument("colDimension", help="Number of columns", action="store", type=int)
	parser.add_argument("numMines", help="Number of mines", action="store", type=int)

	args = parser.parse_args()

	numFiles = args.numFiles
	filename = args.filename
	rowDimension = args.rowDimension
	colDimension = args.colDimension
	numMines = args.numMines
	
	if (rowDimension >= 4 and colDimension >= 4 and (numMines <= rowDimension*colDimension - 9) and numMines >= 1):
		generateWorlds(numFiles, filename, rowDimension, colDimension, numMines)
	else:
		print("ERROR: Could not generate worlds! \n\trowDimension >= 4, colDimension >= 4, 1 <= numMines <= (rowDimension*colDimension - 9)")


if __name__ == "__main__":
	main()
	
