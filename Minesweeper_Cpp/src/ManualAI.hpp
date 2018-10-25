// ======================================================================
// FILE:        ManualAI.hpp
//
// AUTHOR:      Jian Li
//
// DESCRIPTION: This file contains the manual agent class, which
//              implements the agent interface. The ManualAI will allow
//              you to play the game as an omniscient agent. This will
//              allow you to get a feel for the game before starting to
//              code your agent.
//
// NOTES:       - The 'Get Input' part of the code will ignore all info
//                after the first letter, as well as, all whitespace
//                before the first letter.
//
//              - The 'Print Command Menu' part of the code states that
//                'L' will return the LEAVE action.
//
//              - Don't make changes to this file.
// ======================================================================

#ifndef MINE_SWEEPER_CPP_SHELL_MANUALAI_HPP
#define MINE_SWEEPER_CPP_SHELL_MANUALAI_HPP

#include "Agent.hpp"
#include<iostream>

class ManualAI : public Agent
{
public:

    ManualAI ( int _rowDimension, int _colDimension, int _totalMines, int _agentX, int _agentY ){
        rowDimension = _rowDimension;
        colDimension = _colDimension;
        totalMines   = _totalMines;
    };

    Action getAction( int number ) override
    {
        // Print Command Menu
        std::cout << "---------------- Available Actions ----------------" << std::endl;
        std::cout << "L: leave game   U: uncover tile   F: flag   N: unflag" << std::endl;

        Action_type new_action = Action_type ::LEAVE;
        char input_action;
        int input_x = -1; // x = col
        int input_y = -1; // y = row

        // get action from input
        std::cout << "Enter a action:  ";
        while (true)
        {

            std::cin >> input_action;
            std::cin.ignore(9999, '\n');


            if (input_action == 'L')
                break;
            else if (input_action == 'U')
            {
                new_action = UNCOVER;
                break;
            }

            else if (input_action == 'F')
            {
                new_action = FLAG;
                break;
            }

            else if (input_action == 'N')
            {
                new_action = UNFLAG;
                break;
            }

            else
                std::cout << "Invalid action specified, please enter again: ";
        }

        // get coordinates from input
        if (new_action != LEAVE)
        {
            std::cout << "Enter X: ";
            while (!(std::cin >> input_x) || !std::cin.good() || input_x < 1 || input_x > rowDimension)
            {
                std::cout << "Invalid X coordinate specified, please enter again: ";
                std::cin.clear();
                std::cin.ignore(9999,'\n');
            }
            std::cin.ignore(9999,'\n');
            std::cout << "Enter Y: ";
            while (!(std::cin >> input_y) || input_y < 1 || input_y > colDimension)
            {
                std::cout << "Invalid Y coordinate specified, please enter again: ";
                std::cin.clear();
                std::cin.ignore(9999,'\n');
            }
            std::cin.ignore(9999,'\n');
        }

        return {new_action, input_x - 1, input_y - 1};
    };
};


#endif //MINE_SWEEPER_CPP_SHELL_MANUALAI_HPP
