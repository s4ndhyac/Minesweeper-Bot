package src;
import java.util.Arrays;
import java.util.Scanner;

public class ManualAI extends AI {
	
	public Action getAction(int number) {
		Scanner scanner = new Scanner(System.in);
		String actionStr = "", coordStr = "";
		int row = -1, col = -1;
		boolean valid = false;
		// Prompt user for input (loop until valid input given)
		while (!valid) {
			actionStr = scanner.nextLine().toUpperCase();
			if (actionStr.equals("L")) {
				return new Action(Action.ACTION.LEAVE,1,1);
			} else if (actionStr.equals("U") || actionStr.equals("F") || actionStr.equals("N")) {
				System.out.print("Enter (x,y) coordinate (w/out the parentheses): ");
				coordStr = scanner.nextLine();
				String[] coords = coordStr.split(",");
				try {
					row = Integer.parseInt(coords[0]);
					col = Integer.parseInt(coords[1]);
				} catch (Exception e) {
					System.out.println("Illegal Coordinates: Coordinates must have format int,int. Exiting.");
					System.exit(1);
					continue;
				}			
				valid = true;
			} else {
				System.out.println("Illegal Action! Exiting.");
				System.exit(1);
			}
		}
		if (actionStr.equals("U")) {
			return new Action(Action.ACTION.UNCOVER, row, col);
		}
		else if (actionStr.equals("F")) {
			return new Action(Action.ACTION.FLAG, row, col);
		} 
		else {
			return new Action(Action.ACTION.UNFLAG, row, col);
		}
	}
	
	public static void printArray(String[] coords) {
		for (int i = 0; i < coords.length; i++) {
			System.out.print("element " + i + ": " + coords[i] + " ");
		}
		System.out.println();
	}
}
