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
	
	@Test public void testMiddles() throws Exception {
		Board board = new Board(3);
		ArtificialAgentSimple ai = new ArtificialAgentSimple(MarkTypeEnum.O);
		board.mark(1, MarkTypeEnum.X);
		board.mark(3, MarkTypeEnum.X);
		board.mark(4, MarkTypeEnum.O);//need because simplistic a.i. would never allow
		//the above case to occur without putting its mark in the middle slot
		ai.turn(board);
		assertEquals(ai.getMarkType(), board.getBoard()[0]);
	}

	@Test public void testRandom() throws Exception {
		ArtificialAgentSimple ai = new ArtificialAgentSimple(MarkTypeEnum.O);
		ArtificialAgentRandom rand = new ArtificialAgentRandom(MarkTypeEnum.X);
		testRun(ai, rand, MarkTypeEnum.X);//ai goes first
		testRun(rand, ai, MarkTypeEnum.X);//random goes first
	}

	@Test public void testParse() throws Exception {
		ArtificialAgentSimple ai = new ArtificialAgentSimple(MarkTypeEnum.O);
		Board board = new Board(3);
		board.execute("X4,O0,X3,O5,X8,O6,X1");
		ai.turn(board);
		assertEquals(board.getBoard()[7], ai.getMarkType());
	}

	public void testRun(Agent first, Agent second, MarkTypeEnum enemy) throws Exception {
		for(int i=0; i<99999; i++){
			Board board = new Board(3);
			MarkTypeEnum winner = MarkTypeEnum.NONE;
			while(winner == MarkTypeEnum.NONE){
				first.turn(board);
				winner = board.getWinner();
				if(winner == MarkTypeEnum.NONE){
					second.turn(board);
					winner = board.getWinner();
				}
			}
			System.out.println("Testing win on iteration " + i + " for:\n" + board +
					"\nmoves: " + board.getMoves());
			assertFalse(winner == enemy);
		}
	}
}
