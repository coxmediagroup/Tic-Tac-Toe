package com.blastedstudios.tictactoe.agent;

import static org.junit.Assert.*;

import org.junit.Test;

import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

public class ArtificialAgentSimpleTest {
	@Test public void testSimple() throws Exception {
		Board board = new Board(3);
		ArtificialAgentSimple ai = new ArtificialAgentSimple(MarkTypeEnum.O);
		board.mark(0, MarkTypeEnum.X);
		board.mark(2, MarkTypeEnum.X);
		board.mark(4, MarkTypeEnum.O);//need because simplistic a.i. would never allow
		//the above case to occur without putting its mark in the middle slot
		ai.turn(board);
		assertEquals(ai.getMarkType(), board.getBoard()[1]);
	}
}
