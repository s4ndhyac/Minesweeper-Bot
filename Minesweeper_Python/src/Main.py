# ==============================CS-199==================================
# FILE:			Main.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file is the entry point for the program. The main
#				function serves a few purposes: (1) It is the command
#				line interface. (2) It reads the Minesweeper World file,
#				creates the corresponding World object, passes the
#				necessary information, and runs the world. (3) It outputs
#				information regarding the performance of your agent.
#
# NOTES: 		- Syntax:
#
#					Minesweeper [Options]
#
#					Options:
#						-m Use ManualAI instead of MyAI.
#						-r Use RandomAI instead of MyAI.
#						-f [InputPath] [OutputFile]
#						   First is absolute path to Minesweeper World file or 
#						   directory containing Minesweeper World files.
#						   Second is the file name of the .txt file you wish
#						   to write your results to.
#						-v Verbose mode displays the name of the Minesweeper
#						   World file before running on that world.
#						-d Debug mode will display the game board after
#						   every move. Useless when used with -m.
#						-o Path to output file which results are written to.
#						-h Displays help menu and quits.
#
#				- The default AI type is MyAI.
#				
#				- When using -f, the [OutputFile] should only be used when
#				  [InputPath] is a folder of world files. If not, then
#				  [OutputPath] is useless.
#
#				- If both -m and -r are turned on, -r will be turned off.
#				- -v used without -f is useless.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import sys
import os
import argparse
from World import World
from ManualAI import ManualAI
from RandomAI import RandomAI
from MyAI import MyAI


def main():

	# Create parser
	parser = argparse.ArgumentParser(description="", prog="Main.py", usage="%(prog)s [options]", epilog="Note: [options] can be in any order")

	# Parse options																				# Help is default
	parser.add_argument("-f", "-F", help="file or directory name", nargs='*')								# File path
	parser.add_argument("-m", "-M", help="enable ManualAI mode", action="store_true")			# ManualAI
	parser.add_argument("-r", "-R", help="enable RandomAI mode", action="store_true")			# RandomAI
	parser.add_argument("-v", "-V", help="enable verbose mode", action="store_true")			# Verbose
	parser.add_argument("-d", "-D", help="enable debug mode", action="store_true")				# Debug

	args = parser.parse_args()
	
	inputFile = None
	outputFile = None
	filepath = args.f
	if filepath:
		if len(filepath) == 2:
			inputFile = filepath[0]
			outputFile = filepath[1]
		elif len(filepath) == 1:
			inputFile = filepath[0]
		else:
			print("ERROR: -f takes 1 or 2 arguments only!")
			return
	verbose = args.v
	debug = args.d

	if args.m:
		aiType = "manual"
	elif args.r:
		aiType = "random"
	elif not args.m and not args.r:
		aiType = "myai"

	if inputFile:
		# If inputFile is a directory
		if (os.path.isdir(inputFile)):
			listOfWorlds = None

			try:
				directory = os.walk(inputFile)
			except:
				print("ERROR: Failed to open directory")
				return

			numScores = 0
			sumScores = 0

			scoreBeg = 0
			scoreInt = 0
			scoreExp = 0
			for dirpath, _, filenames in directory:
				for filename in filenames:
					f = os.path.join(dirpath, filename)

					world = World(filename=f, aiType=aiType, verbose=verbose, debug=debug)

					score = world.run()
					if score == 1:
						scoreBeg += 1
					elif score == 2:
						scoreInt += 1
					elif score == 3:
						scoreExp += 1

					numScores += 1
					sumScores += score
					
			print("---------------Your agent's results:---------------")
			print("Beginner: {} \tIntermediate: {} \tExpert: {}".format(scoreBeg, scoreInt, scoreExp))
			print("Cumulative Score: " + str(sumScores))

			if outputFile:
				currDirectory = os.path.dirname(__file__)
				outputFilePath = os.path.join(currDirectory, outputFile)
				print(outputFilePath)
				try:
					with open(outputFilePath, 'w') as file:
						file.write("easy: " + str(scoreBeg) + "\n")
						file.write("medium: " + str(scoreInt) + "\n")
						file.write("expert: " + str(scoreExp) + "\n")
						file.write("score: " + str(sumScores))
				except:
					print("ERROR: Could not open file for writing!")

		# If inputFile is a world file
		elif (os.path.isfile(inputFile)):
			world = World(filename=inputFile, aiType=aiType, verbose=verbose, debug=debug)
			score = world.run()
			if score > 0:
			    print("WORLD COMPLETE")
			else:
			    print("WORLD INCOMPLETE")

		# If inputFileis an invalid path
		else:
			print("ERROR: Directory or file does not exist!")

	else:
		world = World(aiType=aiType, verbose=verbose, debug=debug)
		score = world.run()
		print("Your AI scored: " + str(score))
		if score == 0:
			print("WORLD INCOMPLETE")
		else:
			print("WORLD COMPLETE")
		

if __name__ == "__main__":
	main()
