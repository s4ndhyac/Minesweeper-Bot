package src;

import org.apache.commons.cli.*;
import java.io.*;

public class Main {
	public static void main(String[] args) throws Exception {
		String aiType = "myai";
		boolean debug_mode = false;
        boolean verbose_mode = false;
		World world = null;
		// ------------------------- Parse Options ---------------------------
        Options options = new Options();
        
        Option help = new Option("h", "help", false, "help");
        help.setRequired(false);
        options.addOption(help);
        
        Option file = new Option("f", "file", true, "file input");
        file.setRequired(false);
        file.setOptionalArg(true);
        file.setArgs(2);
        options.addOption(file);

        Option manualMode = new Option("m", "manual", false, "manual mode");
        manualMode.setRequired(false);
        options.addOption(manualMode);
        
        Option randomMode = new Option("r", "random", false, "random mode");
        randomMode.setRequired(false);
        options.addOption(randomMode);
        
        Option verbose = new Option("v", "verbose", false, "verbose mode");
        verbose.setRequired(false);
        options.addOption(verbose);
        
        Option debug = new Option("d", "debug", false, "debug mode");
        debug.setRequired(false);
        options.addOption(debug);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("Minesweeper", options);
            System.exit(1);
        }
        
        if (cmd.hasOption("help")) {
        	formatter.printHelp("Usage", options);
        	System.exit(0);
        }

        
        // first arg is filename, second is output file name (if provided)
        String[] files = cmd.getOptionValues("file");
        String filename = null;
        String outputFile = null;
        if (files != null) {
            filename = files[0];
            outputFile = null;
            if (files.length > 1) {
                outputFile = files[1];
            }
        }
        
        // Random AI has priority over Manual AI if both flags are given
        if (cmd.hasOption("random")) {
        	aiType = "random";
        } else if (cmd.hasOption("manual")) {
        	aiType = "manual";
        }
        
        if (cmd.hasOption("debug")) {
        	debug_mode = true;
        }

        if (cmd.hasOption("verbose")) {
            verbose_mode = true;
        }

        // ------------------------- Create World ---------------------------
        int totalScore = 0;
        int easy_comp = 0;
        int med_comp = 0;
        int expert_comp = 0;
        int totalWorlds = 0;

		if (filename != null) {
			File f = new File(filename);
			if (f.isDirectory()) {
				System.out.println("Running on Worlds in... " + filename);
				File worldsDir = new File(filename);
				for (File worldFile : worldsDir.listFiles()) {
                    if (verbose_mode) {
                        System.out.println("Running on " + worldFile.getCanonicalPath());
                    }
                    totalWorlds++;
					world = new World(worldFile.getCanonicalPath(), aiType, debug_mode);
					// double score = world.run();
                    World.Results results = world.run();
                    double score = results.score;
                    int difficulty = results.difficulty;
					if (score > 0) {
                        totalScore += score;
                        // sqScore += score*score;
						//System.out.println("compled difficulty: " + results.difficulty);
                        if (difficulty == 1) {
                            easy_comp++;
                        } else if (difficulty == 2) {
                            med_comp++;
                        } else if (difficulty == 3) {
                            expert_comp++;
                        }
					}
                    if (outputFile != null) {
                        f = new File(outputFile);
                        PrintWriter output = new PrintWriter(f);
                        output.println("easy: " + easy_comp);
                        output.println("medium: " + med_comp);
                        output.println("expert: " + expert_comp);
                        output.println("score: " + totalScore);
                        output.close();
                    }
				}
                
                System.out.println("---------- Stats: -----------");
                System.out.println("Total Worlds: " + totalWorlds);
				System.out.println("Easy Completion: " + easy_comp);
                System.out.println("Medium Completion: " + med_comp);
                System.out.println("Expert Completion: " + expert_comp);
                System.out.println("Total Score: " + totalScore);
                // System.out.println("Std. Deviation: " + stdDev);
			} else if (f.isFile()) {
				System.out.println("Running on world " + filename);
				world = new World(filename, aiType, debug_mode);
				world.run();
			}
		} else {
			System.out.println("Running on random world...");
			world = new World(null, aiType, debug_mode);
			world.run();
            world.printBoardInfo();
		}
	}

}
