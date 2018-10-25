# ==============================CS-199==================================
# FILE:			Action.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the Action class. This class stores
#				action (from the Action Enum in AI.py) and the coordindates
#				of the action.
#
# NOTES: 		- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

class Action():

	def __init__(self, action, x=1, y=1):
		""" Default values of x and y are 1 for LEAVE """
		self.__action = action
		self.__x = x
		self.__y = y

	def getMove(self) -> "Action Object":
		""" Allow private variable action to be publicly accessible """
		return self.__action

	def getX(self) -> int:
		""" Allow private variable x to be publicly accessible """
		return self.__x

	def getY(self) -> int:
		""" Allow private variable y to be publicly accessible """
		return self.__y