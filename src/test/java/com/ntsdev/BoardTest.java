package com.ntsdev;

import com.ntsdev.game.Board;
import com.ntsdev.game.CellState;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class BoardTest {

    @Test
    public void testBoardInitializedToAllBlank(){
        Board board = new Board();
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                assertEquals("Cell wasn't blank", board.getState(i, j), CellState.BLANK);
            }
        }
    }

    @Test
    public void testValidMoveSuccessful(){
        Board board = new Board();
        boolean success = board.makeMove(0,0,CellState.X);
        assertTrue("Move unsuccessful", success);
        assertEquals("Move unrecorded", board.getState(0, 0), CellState.X);
    }

    @Test
    public void testInvalidMoveUnsuccessful(){
        Board board = new Board();
        board.makeMove(0,0,CellState.X);
        boolean success = board.makeMove(0,0,CellState.O);
        assertFalse("Invalid move successful", success);
    }

}
