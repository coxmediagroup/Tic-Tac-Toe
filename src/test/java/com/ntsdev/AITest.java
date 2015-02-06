package com.ntsdev;

import com.ntsdev.game.AI;
import com.ntsdev.game.Board;
import com.ntsdev.game.CellState;
import com.ntsdev.game.Position;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class AITest {

    @Test
    public void testHorizontalWin(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,0),CellState.X);
        board.setState(Position.withCoordinates(1,0),CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(2,0,board,CellState.X);

        assertTrue("Winning move not identified", winning);
    }

    @Test
    public void testVerticalWin(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,0),CellState.X);
        board.setState(Position.withCoordinates(0,1),CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(0,2,board,CellState.X);

        assertTrue("Winning move not identified", winning);
    }

    @Test
    public void testDiagonalWinTopLeftToBottomRight(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,0),CellState.X);
        board.setState(Position.withCoordinates(1,1),CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(2,2,board,CellState.X);

        assertTrue("Winning move not identified", winning);
    }

    @Test
    public void testDiagonalWinTopRightToBottomLeft(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,2),CellState.X);
        board.setState(Position.withCoordinates(1,1),CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(2,0,board,CellState.X);

        assertTrue("Winning move not identified", winning);
    }

    @Test
    public void testNonWinningMove(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,2),CellState.X);
        board.setState(Position.withCoordinates(1,1),CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(0,0,board,CellState.X);

        assertFalse("Non-winning move not identified", winning);
    }

    @Test
    public void testComputerPlaysWinningMoveDiagonally(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,2),CellState.X);
        board.setState(Position.withCoordinates(1,1),CellState.X);

        AI ai = new AI();
        Board newBoard = ai.makeMove(board);

        CellState winner = newBoard.checkWinner();

        assertEquals("Computer didn't win", winner, CellState.X);
    }

    @Test
    public void testComputerPlaysWinningMoveVertically(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,0),CellState.X);
        board.setState(Position.withCoordinates(1,0),CellState.X);

        AI ai = new AI();
        Board newBoard = ai.makeMove(board);

        CellState winner = newBoard.checkWinner();

        assertEquals("Computer didn't win", winner, CellState.X);
    }

    @Test
    public void testComputerPlaysWinningMoveHorizontally(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,0),CellState.X);
        board.setState(Position.withCoordinates(0,1),CellState.X);

        AI ai = new AI();
        Board newBoard = ai.makeMove(board);

        CellState winner = newBoard.checkWinner();

        assertEquals("Computer didn't win", winner, CellState.X);
    }

    @Test
    public void testComputerBlocksPlayerFromWinning(){
        Board board = new Board();
        board.setState(Position.withCoordinates(0,0),CellState.O);
        board.setState(Position.withCoordinates(0,1),CellState.O);

        AI ai = new AI();
        Board newBoard = ai.makeMove(board);

        assertEquals("Computer didn't block player", newBoard.getState(Position.withCoordinates(0,2)), CellState.X);
    }

}
