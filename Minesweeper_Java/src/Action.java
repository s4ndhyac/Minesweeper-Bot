package src;


public class Action {
	public enum ACTION {
		LEAVE, UNCOVER, FLAG, UNFLAG
	};
	
	public ACTION action;
	public int x;
	public int y;

	public Action(ACTION action, int x, int y) {
		this.action = action;
		this.x = x;
		this.y = y;
	}
	
	public Action(ACTION action) {
		this.action = action;
		this.x = this.y = 1;
	}

	public String toString() {
		String retString = this.action + " ";
		if (this.action != ACTION.LEAVE) {
			retString = retString + "(" + this.x + "," + this.y + ")";
		}
		return retString;
		
	}
}
