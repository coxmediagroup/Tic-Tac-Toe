package com.ntsdev;

import com.ntsdev.game.AI;
import com.ntsdev.game.Board;
import com.ntsdev.game.CellState;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class AITest {

    @Test
    public void testHorizontalWin(){
        Board board = new Board();
        board.setState(0,0,CellState.X);
        board.setState(1,0,CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(2,0,board,CellState.X);

        assertTrue("Winning move not identified", winning);
    }

    @Test
    public void testVerticalWin(){
        Board board = new Board();
        board.setState(0,0,CellState.X);
        board.setState(0,1,CellState.X);

        AI ai = new AI();
        boolean winning = ai.isWinningMove(0,2,board,CellState.X);

        assertTrue("Winning move not identified", winning);
    }
}
