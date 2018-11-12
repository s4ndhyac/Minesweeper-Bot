# ==============================CS-199==================================
# FILE:                 MyAI.py
#
# AUTHOR:               Justin Chung
#
# DESCRIPTION:  This file contains the MyAI class. You will implement your
#                               agent in this file. You will write the 'getAction' function,
#                               the constructor, and any additional helper functions.
#
# NOTES:                - MyAI inherits from the abstract AI class in AI.py.
#
#                               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

        def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

                ########################################################################
                #                                                       YOUR CODE BEGINS                                                   #
                ########################################################################
                self.__size = rowDimension * colDimension
                self.__node_weights = [0]*(self.__size)
                self.__length = colDimension
                self.__unexplored = [i for i in range(self.__size)]
                self.__minecount = totalMines
                self.__x = startX
                self.__y = startY
                pass
                ########################################################################
                #                                                       YOUR CODE ENDS                                                     #
                ########################################################################
        def neighbour_finder(self, index):
            neighbour_list = []
            temp = index + 1
            if temp % self.__length != 0:
                neighbour_list.append(temp)
            temp = index - 1
            if (temp + 1) % self.__length != 0:
                neighbour_list.append(temp)
            temp_index = index + self.__length
            if temp_index < self.__size:
                neighbour_list.append(temp_index)
                temp = temp_index + 1
                if temp % self.__length != 0:
                    neighbour_list.append(temp)
                temp = temp_index -1
                if (temp + 1) % self.__length != 0:
                    neighbour_list.append(temp)
            temp_index = index - self.__length
            if temp_index >= 0:
                neighbour_list.append(temp_index)
                temp = temp_index + 1
                if temp % self.__length != 0:
                    neighbour_list.append(temp)
                temp = temp_index - 1
                if (temp + 1) % self.__length != 0:
                    neighbour_list.append(temp)
            return neighbour_list

        def list2coord_Converter(self, index):
                x = index // self.__length
                y = index % self.__length
                return (x+1,y+1)

        def coord2list_Converter(self, x, y):
                return (x-1)*self.__length + (y-1)

        def getAction(self, number: int) -> "Action Object":

                ########################################################################
                #                                                       YOUR CODE BEGINS                                                   #
                ########################################################################
                if number != -1:
                    list_index = self.coord2list_Converter(self.__x, self.__y)
                    self.__unexplored.remove(list_index)
                    neighbours = self.neighbour_finder(list_index)
                for node in neighbours:
                    self.__node_weights[node] += number
                if len(self.__unexplored) == 0:
                    max_in, max_val = max(self.__node_weights)
                    self.__node_weights[max_in] = -1000
                    self.__x, self.__y = self.list2coord_Converter(node)
                    return Action(AI.Action.FLAG, self.__x, self.__y)
                for node in self.__unexplored:
                    if self.__node_weights[node] == 0:
                        self.__x, self.__y = self.list2coord_Converter(node)
                        break
                return Action(AI.Action.UNCOVER, self.__x, self.__y)
                #return Action(AI.Action.LEAVE)
                ########################################################################
                #                                                       YOUR CODE ENDS                                                     #
                ########################################################################
