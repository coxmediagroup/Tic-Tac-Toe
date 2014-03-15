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

	@Override public void turn(Board board) {
		while(true){
			try{
				int position = getPosition(board);
				if(position != -1){
					board.mark(position, markType);
					return;
				}
				System.out.println("Invalid position!");
			}catch(Exception e){
				System.out.println(e.getMessage());
			}
		}
	}
	
	private int getPosition(Board board){
		String input = System.console().readLine();
		int position = Integer.parseInt(input);
		if(position < 0 || position > board.getBoard().length)
			return -1;
		return position;
	}
}
