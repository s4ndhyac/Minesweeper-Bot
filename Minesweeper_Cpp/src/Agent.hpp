// ======================================================================
// FILE:        Agent.hpp
//
// AUTHOR:      Jian Li
//
// DESCRIPTION: This file contains the abstract agent class, which
//              details the interface for a agent. The actuators
//              are listed in the 'Action_type' enum, while the sensors are
//              parameters to the abstract function 'getAction'. Any
//              agent will need to implement the getAction function,
//              which returns an Action for every turn in the game.
//
// NOTES:       - An agent is anything that can be viewed as perceiving
//                its environment through sensors and acting upon that
//                environment through actuators
//
//              - Throughout this project Agent and AI are
//                interchangeable
//
//              - Don't make changes to this file.
// ======================================================================

#ifndef MINE_SWEEPER_CPP_SHELL_AGENT_HPP
#define MINE_SWEEPER_CPP_SHELL_AGENT_HPP

class Agent {

public:
        int    rowDimension;
        int    colDimension;
        int    totalMines;
        int    agentX;
        int    agentY;
        public:

        // Actuators
        enum Action_type
        {
            LEAVE,
            UNCOVER,
            FLAG,
            UNFLAG,
        };

        struct Action{
            Action_type     action;
            int             x;
            int             y;

        };

        virtual Action getAction
                (
                    int number
                ) = 0;
        };

#endif //MINE_SWEEPER_CPP_SHELL_AGENT_HPP
