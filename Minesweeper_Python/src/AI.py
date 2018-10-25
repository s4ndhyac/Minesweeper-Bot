# ==============================CS-199==================================
# FILE:			AI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the abstract AI class, which details
#				the interface for a Minesweeper agent. The actuators for
#				your agent are listed in the 'Action' enum and the sensors
#				are listed as parameters to the abstract fucntion 'getAction'.
#				Any agent will need to implement the getAction function,
#				which returns an Action for every turn of the game.
#
# NOTES: 		- An agent is anything that canbe viewed as perceiving its
#				  environment through sensors and acting upon that
#				  environment through actuators.
#
#				- Throughout this project Agent and AI are interchangeable.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from abc import ABCMeta, abstractmethod
from enum import Enum, unique


class AI:
	__metaclass__ = ABCMeta

	@unique
	class Action (Enum):
		LEAVE = 0
		UNCOVER = 1
		FLAG = 2
		UNFLAG = 3
		
	@abstractmethod
	def getAction(self, number: int) -> "Action Oject":
		pass
