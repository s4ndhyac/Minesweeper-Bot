// ======================================================================
// FILE:        Main.cpp
//
// AUTHOR:      Jian Li
//
// DESCRIPTION: This file is the entry point for the program. The main
//              function serves a couple purposes: (1) It is the
//              interface with the command line. (2) It reads the files,
//              creates the World object, and passes that all the
//              information necessary. (3) It is in charge of outputing
//              information.
//
// NOTES:       - Syntax:
//
//                	Minesweeper [Options] [InputFile] [OutputFile]
//
//                  Options:
//						-m Use the ManualAI instead of MyAI.
//						-r Use the RandomAI instead of MyAI.
//                      -d Debug mode, which displays the game board
//                         after every mode. Useless with -m.
//                      -v Verbose mode displays world file names before
//                         loading them.
//                      -f Depending on the InputFile format supplied,
//                         this operand will trigger program
//                         1) Treats the InputFile as a folder containing many worlds.
//                         The program will then construct a world for every valid world file found.
//                         The program to display total score instead of a single score.
//                         The InputFile operand must be specified with this option
//                         2) Threats the inputFile as a file.
//                         The program will then construct a world for a single valid world file found.
//                         The program to display a single score.
//
//                  InputFile: A path to a valid Minesweeper File, or
//                             folder with -f.
//
//                  OutputFile: A path to a file where the results will
//                              be written. This is optional.
//
//              - If -m and -r are turned on, -m will be turned off.
//
//              - Don't make changes to this file.
// ======================================================================

#include <iostream>
#include <dirent.h>
#include <cmath>
#include "World.hpp"
#include <sys/stat.h>


using namespace std;

int main( int argc, char *argv[] )
{

    // Set random seed
    srand( time ( NULL ) );

    if ( argc == 1 ){
        World world(false, std::string(), std::string());
        int score = world.run();
        if (score)
            cout << "WORLD COMPLETE" << endl;
        else
            cout <<  "WORLD INCOMPLETE" << endl;
        return 0;
    }

    // Important Variables
    bool 	debug        = false;
    bool	verbose      = false;
    string  aiType       = "MyAI";
    bool 	folder       = false;
    string	worldFile    = "";
    string	outputFile   = "";
    string 	firstToken 	 = argv[1];

    // read options if there are options
    if ( firstToken[0] == '-' )
    {
        // Parse Options
        for (int index = 1; index < firstToken.size(); ++index)
        {
            // If both AI's on, turn one off and let the user know.
            if ( firstToken[index] == '-' )
                    continue;
            if ( firstToken[index] == 'f' || firstToken[index] =='F' )
            {
                struct stat path_stat;
                worldFile = argv[2];
                stat ( worldFile.c_str(), &path_stat );
                folder = S_ISDIR ( path_stat.st_mode );
            }

            if ( firstToken[index] == 'v' || firstToken[index] =='V' )
                verbose = true;
            if ( firstToken[index] == 'r' || firstToken[index] == 'R' )
            {
                if ( aiType == "manualAI" )
                    cout << "[WARNING] Manual AI and Random AI both on;"" Manual AI was turned off." << endl;
                aiType = "randomAI";
            }
            if ( firstToken[index] == 'm' || firstToken[index] == 'M' )
            {
                if ( aiType == "randomAI" )
                    cout << "[WARNING] Manual AI and Random AI both on; Manual AI was turned off." << endl;
                else
                    aiType = "manualAI";
            }
            if (firstToken[index] == 'd' || firstToken[index] == 'D')
                debug = true;

        }


        if ( argc >= 4 )
            outputFile = argv[3];

    }

    // no input folder for -f option turning on
    if ( worldFile == "" )
    {
        if ( folder )
            cout << "[WARNING] No folder specified; running on a random world." << endl;
        World world(debug, aiType, std::string());
        int score = world.run();
        if (score)
            cout << "WORLD COMPLETE" << endl;
        else
            cout <<  "WORLD INCOMPLETE" << endl;
        return 0;
    }



    // no input file or invalid file for -f option turning on
    if ( folder )
    {
        DIR *dir;
        if ((dir = opendir(worldFile.c_str())) == NULL)
        {
            cout << "[ERROR] Failed to open directory." << endl;
            return 0;
        }

        struct dirent *ent;

        double sumOfScores = 0;
        int easy = 0;
        int medium = 0;
        int expert = 0;

        while ((ent = readdir(dir)) != NULL)
        {
            if (ent->d_name[0] == '.')
                continue;
            if (verbose)
                cout << "Running world: " << ent->d_name << endl;

            string individualWorldFile = worldFile + "/" + ent->d_name;

            int score;
            try {
                World world(debug, aiType, individualWorldFile);
                score = world.run();
                if (score == 3)
                    ++expert;
                else if (score == 2)
                    ++medium;
                else if (score == 1)
                    ++easy;
            }
            catch (...) {
                sumOfScores = 0;
                break;
            }

            sumOfScores += score;
        }

        closedir(dir);


        if ( outputFile == "" )
        {

            cout << "easy: " << easy << endl;
            cout << "medium: "  << medium << endl;
            cout << "expert: " << expert << endl;
            cout << "score: " << sumOfScores << endl;
        }
        else
        {
            ofstream file;
            file.open( outputFile );
            file << "easy: "  << easy << endl;
            file << "medium: " << medium << endl;
            file << "expert: " << expert << endl;
            file << "score: " << sumOfScores << endl;
            file.close();
        }
        return 0;
    }


    try
    {
        if ( verbose )
            cout << "Running world: " << worldFile << endl;

        World world(debug, aiType, worldFile);
        int score = world.run();
        if ( outputFile == "" )
        {
            if (score)
                cout << "WORLD COMPLETE" << endl;
            else
                cout <<  "WORLD INCOMPLETE" << endl;
        }
        else
        {
            ofstream file;
            file.open ( outputFile );
            if (score)
                file << "WORLD COMPLETE" << endl;
            else
                file <<  "WORLD INCOMPLETE"  << endl;
            file.close();
        }
    }
    catch ( const std::exception& e )
    {
        cout << "[ERROR] Failure to open file." << endl;
    }
    return 0;
}