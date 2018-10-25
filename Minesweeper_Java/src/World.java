package src;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.*;

import src.Action.ACTION;


/*	Author: John Lu
 */

public class World {
	
	// Defaults
	static final int DEFAULT_COLS = 8;
	static final int DEFAULT_ROWS = 8;
	static final int DEFAULT_MINES = 10;
	
	// world-related instance variables
	private int rowDimension;
	private int colDimension;
	private Tile[][] board;
	private int totalMines = 0;  // the # bombs this board has

	// Agent-related instance variables
	private AI agent;
	private int score;
	private int flagsLeft;
	private int startX;
	private int startY;
	private int perceptNumber;
	private int moves;
	
	// Game Mode
	private boolean debug;
	
	// For faster score calculation and checking game-terminating conditions.
	private int coveredTiles;
	private int correctFlags;
	
	
	private enum GAMESTATE {
		ACTIVE, WON, LOST
	};
	private GAMESTATE gameState;

	// There are three levels
	// 		EASY: 8x8 with 10 mines
	//		MEDIUM: 16x16 with 40 mines
	//		EXPERT: 16x30 with 99 mines
	private enum DIFFICULTY {
		NONE, EASY, MEDIUM, EXPERT
	}

	private DIFFICULTY difficulty;
	
	// ------------------- Inner Class: Tile  --------------------
	/* 	Description:
	 * 	A Tile object represent a "square" on the game board.
	 */
	private class Tile {
		public boolean mine = false;
		public boolean covered = true;
		public boolean flagged = false;
		public int number = 0;
	}
	
	// ---------------- Inner Class: TwoTuple  -------------------
	/* 	Description:
	 * 	A TwoTuple is a length-2 tuple of integers used to represent
	 * 	an (x,y) coordinate or, alternatively, a (row, col) coordinate
	 * 	of a Tile in the board.
	 * 	
	 * 	Additional Info:
	 * 	The internal representation of a board is a 2-d array, 0-indexed 
	 * 	array. However, users, specify locations on the board using 1-indexed
	 * 	(x,y) Cartesian coordinates. 
	 */
	private class TwoTuple {
		public int x;
		public int y;
		public TwoTuple(int x, int y) { this.x = x; this.y = y; }
		
		public String toString() {
			return "(" + x + "," + y + ")";
		}
	}

	// ---------------- Inner Class: Results  -------------------
		/* 	Description:
	 * 	A Results object encapsulates information about the performance
	 *  of the AI on this particular world. It contains:
	 *		- score := the score AI earns on this world
	 *		- difficulty := difficulty of the world {0 := None, 1 := easy, 2 := med, 3 := expert}
	 * 		- moves := total number of moves AI took on this world
	 */
	class Results {
		public int score;
		public int difficulty;
		public int moves;
		public Results(int score, int difficulty, int moves) {
			this.score = score; this.difficulty = difficulty; this.moves = moves;
		}
	}

	// ---------------------------- Constructor -----------------------------	
	public World(String filename, String aiType, boolean debug) throws Exception {
		BufferedReader in;
		TwoTuple mv;
		int stRow, stCol;
		
		this.debug = debug;
		
		if (filename != null) {
			in = new BufferedReader(new FileReader(filename));
			
			// Initialize 2-d array of Tile objects
			createBoard(in);
			
			// Get the first move coordinates
			mv = getFirstMove(in);
			this.startX = mv.x;
			this.startY = mv.y;
			
			// Add mines to board
			addMines(in);
			
		} else {
			// Create a default world
			this.colDimension = DEFAULT_COLS;
			this.rowDimension = DEFAULT_ROWS;
			TwoTuple firstMv = getFirstMove();
			this.startX = firstMv.x;
			this.startY = firstMv.y;
			createRandomBoard(this.startX,this.startY);
		}
		
		// Add tile numbers
		addNumbers();
		
		// All tiles begin as covered
		this.coveredTiles = this.rowDimension * this.colDimension;
		
		// Total flags available equals total number of mines
		this.flagsLeft = this.totalMines;
		
		// Uncover the starting square
		TwoTuple rowCol = this.translateCoordinate(this.startX, this.startY);
		stRow = rowCol.x; 
		stCol = rowCol.y;
		this.uncoverTile(stRow, stCol);

		// Store the numpy on starting tile as agent's first percept
		this.perceptNumber = this.getTile(startX, startY).number;
		
		// Instantiate the proper AI class
		this.agent = createAI(aiType);

		// Get board difficulty
		this.difficulty = getDifficulty(this.rowDimension, this.colDimension, this.totalMines);

		this.moves = 0;  // counts number of moves taken by agent
		this.score = 0;

	}

	private DIFFICULTY getDifficulty(int row, int col, int mines) {
		if (row == 8 && col == 8 && mines == 10) {
			return DIFFICULTY.EASY;
		} else if (row == 16 && col == 16 && mines == 40) {
			return DIFFICULTY.MEDIUM;
		} else if (row == 16 && col == 30 && mines == 99)  {
			return DIFFICULTY.EXPERT;
		} else {
			return DIFFICULTY.EASY;
		}
	}
	
	private AI createAI(String aiType) {
		AI ai = null;
		aiType = aiType.toUpperCase();
		switch (aiType) {
			case "MANUAL":
				ai = new ManualAI();
				break;
			case "RANDOM":
				ai = new RandomAI(this.rowDimension, this.colDimension, this.totalMines);
				break;
			case "MYAI":
				ai = new MyAI(this.rowDimension, this.colDimension, this.totalMines, this.startX, this.startY);
				break;
			default:
				ai = new ManualAI();
		}
		return ai;
	}
	
	// ========================== RUN LOOP ==============================
	public Results run() {
		Action actionObj = null;
		boolean gameOver = false;
		
		// Loop until game is over.
		while (!gameOver) {

			// If # moves exceeds 2 * the board size, terminate with 0 score
			if (this.moves >= 2 * this.colDimension * this.rowDimension) {
				System.out.println("Maximum moves exceeded!");
				new Results(0, this.difficulty.ordinal(), this.moves);
			}

			if (this.debug || this.agent instanceof ManualAI) {
				this.printBoardInfo();
				this.printAgentInfo(actionObj);
			}
			
			if (this.agent instanceof ManualAI) {
				this.printActionInfo();
			}
			// Ask agent for its action
			actionObj = this.agent.getAction(this.perceptNumber);
			System.out.println(actionObj);
			// Check the (x,y) coordinates are valid
			if (!this.isInBounds(actionObj.x, actionObj.y)) {
				System.out.println("out of bound coordinates: (" + actionObj.x + "," + actionObj.y + "). Exiting.");
				System.exit(1);
			};
			
			// If action is uncover a tile, then we will pass in the number on the tile
			// as a percept next turn.
			if (actionObj.action == ACTION.UNCOVER) {
				Tile tile = this.getTile(actionObj.x, actionObj.y);
				this.perceptNumber = tile.number;
			} else {
				this.perceptNumber = -1;
			}

			gameOver = this.doMove(actionObj);
			if (this.debug) {
				System.out.println("Hit any button to Continue...");
				Scanner in = new Scanner(System.in);
				in.nextLine();
			}
		}
		if (this.gameState == GAMESTATE.WON) {
			if (this.difficulty == DIFFICULTY.NONE) {
				// Return 1 if user completes a board size that does not correspond
				// to any of the standard board sizes
				this.score = 1;
			} else {
				this.score += this.difficulty.ordinal();
			}
		}

		this.uncoverAll();
		// System.out.println("Final Action: " + actionObj);
		// System.out.println("Score: " + this.score);
		// System.out.println("difficulty: " + this.difficulty);
		// System.out.println("Moves Taken: " + this.moves);
		return new Results(this.score, this.difficulty.ordinal(), this.moves);
	}
	
	private Tile getTile(int x, int y) {
		int row, col;
		TwoTuple rc = this.translateCoordinate(x, y);
		row = rc.x; col = rc.y;
		Tile tile = this.board[row][col];
		return tile;
	}
	
	// returns true if game is over
	private boolean doMove(Action actionObj) {
		int x, y, row, col;
		this.moves++;
		Action.ACTION action = actionObj.action;
		if (action == Action.ACTION.LEAVE) {
			return true;  // quit game
		}
		x = actionObj.x;
		y = actionObj.y;
		TwoTuple rc = this.translateCoordinate(x, y);
		row = rc.x; col = rc.y;
		Tile tile = this.board[row][col];
		switch (action) {
			case UNCOVER:
				if (tile.mine) {
					this.gameState = GAMESTATE.LOST;
					return true;
				} else {
					this.uncoverTile(row, col);
					// check if all tiles uncovered
					if (this.coveredTiles - this.totalMines == 0) {
						this.gameState = GAMESTATE.WON;
						return true;
					}	
				}
				break;
			case FLAG:
				if (this.flagsLeft > 0) {
					// Do not decrement flag count if tile is already flagged.
					if (!tile.flagged) {
						this.flagsLeft--;
						
						// Check if the flag is on a bomb tile (used for scoring)
						if (tile.mine) {
							this.correctFlags++;
						}
					}
					tile.flagged = true;
				}
				break;
			case UNFLAG:
				// Make sure to not exceed number of starting flags
				if (this.flagsLeft < this.totalMines) {
					// Do not increment flag count if there is no flag on the tile
					if (tile.flagged) {
						this.flagsLeft++;
						
						// Check if flag was on a mine tile (used for scoring)
						if (tile.mine) {
							this.correctFlags--;
						}
					}
					tile.flagged = false;
				}	
		}
		return false;
	}
	
	// ---------------------- World Generating Methods ------------------------
	private void createBoard(BufferedReader in) throws Exception {
		/*	Inputs:
		 * 		in - BufferedReader reading the current world file
		 * 
		 * 	Description:
		 * 	Reads in the board dimensions, row and column, from the 
		 *  world file and initializes the "board" instance variable.
		 */
		String[] dims;
		int nRows, nCols;
		dims = in.readLine().split(" ");
		// Convert dimensions to integers
		nRows = Integer.parseInt(dims[0]);
		nCols = Integer.parseInt(dims[1]);
		
		// Create an empty board of tiles
		this.board = new Tile[nRows][nCols];
		this.rowDimension = nRows;
		this.colDimension = nCols;
		
		// Initialize 2-d array of "empty" Tiles
		this.initEmptyBoard();
	}
	
	private void createRandomBoard(int stX, int stY) {
		/*	Inputs:
		 * 		stX - the starting x coordinate for this world. 
		 * 		stY - the starting y coordinate for this world
		 * 
		 * 	Description:
		 * 	Creates a default board with the given input coordinates
		 * 	as the starting tile. Tiles that border the starting tile
		 * 	are guaranteed to not be mines.
		 *  
		 *  Notes: 
		 *  x,y coordinates are 1-indexed. That is,
		 *  	1 <= x <= colDimension & 1 <= y <= rowDimension
		 */
		this.board = new Tile[DEFAULT_ROWS][DEFAULT_COLS];
		TwoTuple rowCol = this.translateCoordinate(stX, stY);
		int stRow = rowCol.x;
		int stCol = rowCol.y;
		this.initEmptyBoard();
		
		// Add Mines
		int i = DEFAULT_MINES;
		while (i > 0) {
			int r = (int) (Math.random() * this.rowDimension);
			int c = (int) (Math.random() * this.colDimension);
			// Do not place mine adjacent to starting tile
			if (Math.abs(r-stRow) > 1 || Math.abs(c-stCol) > 1) {
				// place only if there isn't already a mine
				if (!this.board[r][c].mine) {
					this.addMine(r, c);
					i--;
				}
			}	
		}
	}
	
	private void initEmptyBoard() {
		/*	Description:
		 * 	Initializes the 2-d "board" instance variable based
		 * 	on current values of rowDimension and colDimension
		 * 	instance variables.
		 */
		for (int i = 0; i < this.rowDimension; i++) {
			for (int j = 0; j < this.colDimension; j++) {
				this.board[i][j] = new Tile();
			}
		}	
	}
	
	private TwoTuple getFirstMove(BufferedReader in) throws Exception {
		/*	Inputs:
		 * 		in - BufferedReader reading the current world file
		 * 
		 * 	Outputs
		 * 		TwoTuple representing the x,y coordinate of the first move
		 * 
		 * 	Description:
		 * 	Reads in the first move from the current world file and returns
		 * 	the coordinates of the first move.
		 * 
		 *  Notes: 
		 *  x,y coordinates are 1-indexed. That is,
		 *  	1 <= x <= colDimension & 1 <= y <= rowDimension
		 */
		String[] startTile;
		int startX, startY;
		// Get the starting tile coordinates
		startTile = in.readLine().split(" ");
		startX = Integer.parseInt(startTile[0]);
		startY = Integer.parseInt(startTile[1]);
		return new TwoTuple(startX, startY);
	}
	
	private TwoTuple getFirstMove() {
		/*	Inputs: None
		 * 
		 * 	Outputs
		 * 		TwoTuple representing the x,y coordinate of the first move
		 * 
		 * 	Description:
		 * 	Randomly picks the starting x and y coordinates and returns the 
		 * 	coordinates as a TwoTuple.
		 * 
		 *  Notes: 
		 *  x,y coordinates are 1-indexed. That is,
		 *  	1 <= x <= colDimension & 1 <= y <= rowDimension
		 */
		int stX, stY;
		stX = (int) (Math.random() * this.colDimension) + 1;
		stY = (int) (Math.random() * this.rowDimension) + 1;
		return new TwoTuple(stX, stY);
	}
	
	// ## Confirm with group
	private void addMines(BufferedReader in) throws Exception {
		/*	Inputs:
		 * 		in - BufferedReader reading the current world file
		 * 
		 * 	Outputs: None
		 * 
		 * 	Description:
		 * 	Reads in the 2-d mine grid from current world file and adds
		 * 	each mine (represented by a "1" in the input file) to the board.
		 */
		int row, col;
		int bomb;
		String line = in.readLine();
		
		row = 0;
		while (line != null) {
			String[] bombs = line.split(" ");
			if (bombs.length != this.colDimension) { /*throw exception*/ }
			col = 0;
			for (int i = 0; i < bombs.length; i++) {
				 bomb = Integer.parseInt(bombs[i]);
				 if (bomb == 1) {
					 this.addMine(row, col);
				 }
				 col++;
			}
			row++;
			line = in.readLine();	
		}
	}
	
	private void addMine(int row, int col) {
		/*	Inputs:
		 * 		row - 0-indexed row number in the board
		 * 		col - 0-indexed col number in the board
		 * 
		 * 	Outputs: None
		 * 
		 * 	Description:
		 * 	Adds mine to the given location of the board and increments
		 * 	total mine count.
		 */
		this.board[row][col].mine = true;
		this.totalMines++;
	}

	private void addNumbers() {	
		/*  Description:
		 * 	Sets the number displayed on each tile, which represents
		 * 	the # of neighboring bombs.
		 */
		for (int i = 0; i < rowDimension; i++) {
			for (int j = 0; j < colDimension; j++) {
				if (this.board[i][j].mine) {
					// Increment each neighbor's bomb count
					int rStart = i-1, rEnd = i+1, cStart = j-1, cEnd = j+1;
					if (i == 0) { rStart++; }
					if (i == rowDimension-1 ) { rEnd--; }
					if (j == 0 ) { cStart++; }
					if (j == colDimension-1 ) { cEnd--; }
					for (int r = rStart; r <= rEnd; r++) {
						for (int c = cStart; c <= cEnd; c++) {
							if (r != i || c != j) {
								this.board[r][c].number++;
							}
						}
					}
				}
			}
		}
	}
	
	private void uncoverTile(int row, int col) {
		/*	Inputs:
		 * 		row - 0-indexed row number in the board
		 * 		col - 0-indexed col number in the board
		 * 
		 * 	Outputs: None
		 * 
		 * 	Description:
		 * 	Uncovers given tile and decrements the count of covered tiles.
		 * 	Also updates the "lastUncoveredTile" instance variable.
		 */
		Tile tile = this.board[row][col];
		if (tile.covered) {
			tile.covered = false;
			this.coveredTiles--;
		}
	}
	
	private void uncoverAll() {
		/*	Inputs: None
		 * 
		 * 	Outputs: None
		 * 
		 * 	Description:
		 * 	Uncovers all tiles
		 */
		for (int i = 0; i < this.rowDimension; i++) {
			for (int j = 0; j < this.colDimension; j++) {
				this.uncoverTile(i, j);
			}
		}
	}
	
	private TwoTuple translateCoordinate(int x, int y) {
		/*	Inputs:
		 * 		x - x coordinate of board
		 * 		y - y coordinate of board 
		 * 
		 * 	Outputs:
		 * 		TwoTuple, t, where:
		 * 			t.x is the corresponding row index in the board
		 * 			t.y is the corresponding col index in the board
		 * 
		 * 	Description:
		 * 	Translates the given (x,y) coordinate to a (row, col) tuple used
		 * 	for indexing into the board instance variable. (See Note below).
		 * 
		 * 	Notes:
		 * 	The internal representation of a board is a 2-d array, 0-indexed 
		 * 	array. However, users, specify locations on the board using 1-indexed
		 * 	(x,y) Cartesian coordinates. 
		 * 	Hence, to access the proper indicies into the board array, a translation 
		 * 	must be performed first.
		 */
		int row = this.rowDimension-y;
		int col = x-1;
		return new TwoTuple(row, col);
	}
	// ------------------- End World Generating Methods ---------------------
	
	// ---------------------- World Printing Methods ------------------------
	public void printWorld() {
		printBoardInfo();
		printAgentInfo(null);
		printActionInfo();
	}
	
	public void printBoardInfo() {
		int yAxisWidth = 4;
		int xLeftOffset = 1;
		int xElementSpacing = 3;
		System.out.println("\n---------------- Game Board ------------------");
		System.out.println();
		for (int i = 0; i < this.rowDimension; i++) {
			// Print Row Number
			//System.out.print(this.rowDimension-i + "|");
			System.out.printf("%"+yAxisWidth+"s", this.rowDimension-i+"|");
			System.out.printf("%-"+xLeftOffset+"s", "");
			for (int j = 0; j < this.colDimension; j++) {
				printTileInfo(i, j);
				System.out.printf("%-"+xElementSpacing+"s", "");
			}
			System.out.println();
		}
		// Print Bottom Line Above Column Numbers
		System.out.printf("%"+yAxisWidth+"s", "");
		System.out.printf("%"+xLeftOffset+"s", "");
		for (int j = 0; j < this.colDimension; j++) {
			System.out.print("-");
			System.out.printf("%-"+xElementSpacing+"s", "");
		}
		System.out.println();
		// Print Column Numbers
		System.out.printf("%"+yAxisWidth+"s", "");
		System.out.printf("%"+xLeftOffset+"s", "");
		for (int i = 1; i < this.colDimension+1; i++) {
			System.out.print(i);
			if (i < 10)
				System.out.printf("%-"+xElementSpacing+"s", "");
			else
				System.out.printf("%-"+(xElementSpacing-1)+"s", "");
		}
		System.out.println();
	}
	
	private void printTileInfo(int row, int col) {
		Tile tile = this.board[row][col];
		if (tile.covered) {
			if (tile.flagged) {
				System.out.print("#");
			} else {
				System.out.print(".");
			}
		} else {
			// Uncovered tile
			if (tile.mine) {
				System.out.print("*");
			} else {
				System.out.print(tile.number);
			}
		}
	}
	
	private void printAgentInfo(Action lastAction) {
		System.out.println("------------------ Percepts ------------------ ");
		System.out.print("Tiles Covered: " + this.coveredTiles + "   ");
		System.out.print("Flags Left: " + this.flagsLeft + "   ");

		// DELETE THIS
		//System.out.print("Correct Flags: " + this.correctFlags + "   ");
		//int incorrectFlags = this.totalMines - this.flagsLeft - this.correctFlags;
		//System.out.print("Incorrect Flags: " + incorrectFlags + "   ");

		if (lastAction != null) {
			System.out.print("Last Action: " + lastAction);
		}
		System.out.println();
		System.out.println();
	}
	
	private void printActionInfo() {
		System.out.println("---------------- Available Actions ----------------");
		System.out.println("L: leave game   U: uncover tile   F: flag   N: unflag ");
		System.out.println("Enter Action: ");
	}
	
	private boolean isInBounds(int x, int y) {
		TwoTuple rowCol = this.translateCoordinate(x, y);
		int row = rowCol.x;
		int col = rowCol.y;
		if (row < 0 || row >= this.rowDimension || 
			col < 0 || col >= this.colDimension) {
			return false;
		}
		return true;
	}
	// ---------------------- End World Printing Methods ----------------------
	
	public String toString() {
		String ret = "";
		ret = ret + "Dimensions: " + this.rowDimension + "x" + this.colDimension;
		ret = ret + "Total Mines: " + this.totalMines;
		return ret;
	}
}
