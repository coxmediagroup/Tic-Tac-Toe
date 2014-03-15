package com.blastedstudios.tictactoe.board;

import static org.junit.Assert.*;

import org.junit.Test;

public class BoardTest {

	@Test public void testInitialize() {
		Board board = new Board(3);
		for(MarkTypeEnum space : board.getBoard())
			if(space == null)
				fail("Space null");
			else if ( space != MarkTypeEnum.NONE)
				fail("Space not none, is " + space.name());
	}

	@Test public void testInitializeWinner() {
		for(int span = 3; span < 10; span++)
			assertEquals(MarkTypeEnum.NONE, new Board(span).getWinner());
	}
	
	@Test public void testWinnerHorizontal() throws Exception {
		for(int span=3; span < 10; span++){
			Board board = new Board(span);
			for(int x=0; x < span-1; x++)
				board.mark(x, MarkTypeEnum.X);
			System.out.println("Testing pre win for span==" + span);
			assertEquals(MarkTypeEnum.NONE, board.getWinner());//verify not won yet
			board.mark(span-1, MarkTypeEnum.X);
			System.out.println("Testing post win for span==" + span);
			assertEquals(MarkTypeEnum.X, board.getWinner());
		}
	}

	@Test public void testWinnerDiagonalTopDown() throws Exception {
		Board board = new Board(3);
		board.mark(0, MarkTypeEnum.X);
		board.mark(4, MarkTypeEnum.X);
		board.mark(8, MarkTypeEnum.X);
		assertEquals(MarkTypeEnum.X, board.getWinner());
	}

	@Test public void testWinnerDiagonalBottomUp() throws Exception {
		Board board = new Board(3);
		board.mark(6, MarkTypeEnum.X);
		board.mark(4, MarkTypeEnum.X);
		board.mark(2, MarkTypeEnum.X);
		assertEquals(MarkTypeEnum.X, board.getWinner());
	}
	
	@Test public void testWinnerDiagonal() throws Exception {
		for(int span=3; span < 10; span++){
			Board board = new Board(span);
			for(int x=0; x<span; x++)
				board.mark(x*span+x, MarkTypeEnum.O);
			System.out.println("Testing diagonal for span==" + span);
			assertEquals(MarkTypeEnum.O, board.getWinner());
		}
	}
}
