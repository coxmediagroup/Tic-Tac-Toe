package com.blastedstudios.tictactoe.agent;

import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

/**
 * An agent whose turn is based around keyboard input form terminal
 */
public class TerminalAgent extends Agent{
	public TerminalAgent(MarkTypeEnum markType) {
		super(markType);
	}

	@Override public int turn(Board board) {
		while(true){
			try{
				int location = getLocation(board);
				if(location != -1){
					board.mark(location, markType);
					return location;
				}
				System.out.println("Invalid position!");
			}catch(Exception e){
				System.out.println(e.getMessage());
			}
		}
	}
	
	private int getLocation(Board board){
		String input = System.console().readLine();
		int location = Integer.parseInt(input);
		if(location < 0 || location > board.getBoard().length)
			return -1;
		return location;
	}
}
