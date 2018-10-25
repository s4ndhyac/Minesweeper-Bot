package src;

import src.Action.ACTION;

public class RandomAI extends AI {
	private final int ROW_DIMENSION;
	private final int COL_DIMENSION;
	private final int TOTAL_MINES;
	private int flagsLeft;
	public RandomAI(int rowDimension, int colDimension, int totalMines) {
		this.ROW_DIMENSION = rowDimension;
		this.COL_DIMENSION = colDimension;
		this.TOTAL_MINES = this.flagsLeft = totalMines;
	}
	
	// Make 3 random moves and then leave
	int count = 3;
	ACTION actions[] = ACTION.values();
	// --------------------- Implement getAction() --------------------
	public Action getAction(int number) {
		int idx, x, y;
		while (count > 0) {
			count--;
			// Get a random action that is not LEAVE
			idx = (int)(Math.random() * (actions.length-1)) + 1;
			ACTION action = actions[idx];
			
			x = (int)(Math.random() * this.ROW_DIMENSION) + 1;
			y = (int)(Math.random() * this.COL_DIMENSION) + 1;
			
			return new Action(action,x,y);
		}
		return new Action(ACTION.LEAVE);	
	}
	
}
