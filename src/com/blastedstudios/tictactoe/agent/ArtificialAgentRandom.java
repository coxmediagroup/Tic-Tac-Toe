package com.blastedstudios.tictactoe.agent;

import java.util.Random;

import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

/**
 * Random agent, who picks whatever is not already marked and marks it.
 * Makes testing a little easier, and is the simplest kind of agent.
 */
public class ArtificialAgentRandom extends Agent{
	private final Random random = new Random();
	
	public ArtificialAgentRandom(MarkTypeEnum markType) {
		super(markType);
	}

	@Override public void turn(Board board) {
		int location = -1;
		do{
			location = random.nextInt(board.getBoard().length);
		}while(board.isMarked(location));
		try {
			board.mark(location, markType);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
