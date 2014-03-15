package com.blastedstudios.tictactoe.board;

/**
 * Friday night, 21:14, ~30 minutes after fork
 * 
 * Board class for tic-tac-toe. Initially I was thinking easymode array, but upon
 * reflection, I wondered how extensible we could want this. I considered a.i. implications
 * as a result of making it variable width, a la 4 width tic tac toe, or variable width
 * and different win conditions, a la connect four.
 * 
 * For a brief while I considered my potential enjoyment of making a connect four a.i.,
 * with a decision tree built on startup and continuous pruning each turn. This could work 
 * for tic-tac-toe, variable width, and variable iwn conditions. I don't know
 * what cox is going for here yet, as this is the first twenty minutes or so, but seeing as 
 * how this is a (I don't want to say trivial) easier exercise, they are probably looking
 * for thought process, in which case I should turn this out before they reject me with
 * "noob array java (ab)user" before I do my python/django implementation.
 * 
 * First step: make the board class, test it, verify I know if an agent (ai/human) wins or not.
 * For now I'll go easy as I'm probably over-thinking. I've been balancing how agile I should
 * show this and that I don't add needlessly complex code on the one hand, vs extensible 
 * design that could work for variable width tic tac toe, or connect four/connect five/
 * connect infinity. Dat psychological warfare...
 */
public class Board {
	private final int span;
	private final MarkTypeEnum[] board;
	
	public Board(int span){
		this.span = span;
		board = new MarkTypeEnum[span*span];
		reset();
	}
	
	/**
	 * Change value on board to given space
	 * @throws Exception if marking a spot which is already marked
	 */
	public void mark(int location, MarkTypeEnum space) throws Exception{
		if(board[location] != MarkTypeEnum.NONE)
			throw new Exception("Can't mark place on board which has been previously marked!");
		board[location] = space;
	}
	
	public void reset(){
		for(int i=0; i<board.length; i++)
			board[i] = MarkTypeEnum.NONE;
	}
	
	/**
	 * Scan if anyone has won yet
	 * @return the winner, or NONE if no one has won yet 
	 */
	public MarkTypeEnum getWinner(){
		MarkTypeEnum winner = getWinner(false);
		if(winner == MarkTypeEnum.NONE)
			winner = getWinner(true);
		if(winner == MarkTypeEnum.NONE)
			winner = getWinnerDiagonal();
		return winner;
	}

	private MarkTypeEnum getWinnerDiagonal(){
		//if diagonal, must go through middle, so seed there
		MarkTypeEnum middle = board[span*(span/2)+span/2];
		if(isWinnerDiagonal(middle, true) || isWinnerDiagonal(middle, false))
			return middle;
		return MarkTypeEnum.NONE;
	}
	
	private boolean isWinnerDiagonal(MarkTypeEnum type, boolean topDown){
		boolean win = true;
		int start = topDown ? 0 : board.length - span;
		int stride =  topDown ? span+1 : -span-1;
		for(int x=start; x<board.length && x>=0; x+=stride)
			win &= board[x] == type;
		return win;
	}
	
	private MarkTypeEnum getWinner(boolean vertical){
		for(int i=0; i<span; i++){
			//start with left/top mark, if different, no one wins this row
			MarkTypeEnum type = board[vertical ? i*span : i];
			if(type != MarkTypeEnum.NONE && isWinnerRow(vertical, i, type))
				return type;
		}
		return MarkTypeEnum.NONE;
	}
	
	private boolean isWinnerRow(boolean vertical, int y, MarkTypeEnum type){
		for(int x = 1; x<span; x++)
			if(type != board[vertical ? x*span+y : + y*span+x])
				return false;
		return true;
	}
	
	public MarkTypeEnum[] getBoard() {
		return board;
	}
	
	public String toString(){
		//make top frame
		StringBuffer buffer = new StringBuffer();
		for(int dashes=0; dashes<span+2; dashes++)
			buffer.append("-");
		buffer.append("\n");
		
		//populate middle
		for(int y=0; y<span; y++){
			buffer.append("|");
			for(int x=0; x<span; x++)
				buffer.append(board[y*span + x].printed());
			buffer.append("|\n");
		}

		//make bottom frame
		for(int dashes=0; dashes<span+2; dashes++)
			buffer.append("-");
		return buffer.toString();
	}

	public int getSpan() {
		return span;
	}
}
