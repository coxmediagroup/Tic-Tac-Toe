package com.ntsdev;

import com.ntsdev.game.Board;
import com.ntsdev.game.CellState;
import com.ntsdev.game.Position;
import org.junit.Test;

import static org.junit.Assert.*;

public class BoardTest {

    @Test
    public void testBoardInitializedToAllBlank() {
        Board board = new Board();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                assertEquals("Cell wasn't blank", board.getState(Position.withCoordinates(i, j)), CellState.BLANK);
            }
        }
    }

    @Test
    public void testValidMoveSuccessful() {
        Board board = new Board();
        boolean success = board.makeMove(Position.withCoordinates(0, 0), CellState.X);
        assertTrue("Move unsuccessful", success);
        assertEquals("Move unrecorded", board.getState(Position.withCoordinates(0, 0)), CellState.X);
    }

    @Test
    public void testInvalidMoveUnsuccessful() {
        Board board = new Board();
        board.makeMove(Position.withCoordinates(0, 0), CellState.X);
        boolean success = board.makeMove(Position.withCoordinates(0, 0), CellState.O);
        assertFalse("Invalid move successful", success);
    }

    @Test
    public void testCopyIsExact() {
        Board board = new Board();
        board.makeMove(Position.withCoordinates(0, 0), CellState.X);
        board.makeMove(Position.withCoordinates(2, 2), CellState.X);

        Board copy = board.copy();
        assertEquals("Move not copied", copy.getState(Position.withCoordinates(0, 0)), CellState.X);
        assertEquals("Move not copied", copy.getState(Position.withCoordinates(2, 2)), CellState.X);
    }

    @Test
    public void testBoardJson() {
        Board board = new Board();
        board.setState(Position.withCoordinates(0, 0), CellState.X);
        board.setState(Position.withCoordinates(2, 2), CellState.X);
        String testString = "{\"board\":[[\"X\",\"_\",\"_\"],[\"_\",\"_\",\"_\"],[\"_\",\"_\",\"X\"]]}";
        String boardString = board.toJSON();
        assertEquals("JSON didn't match", testString, boardString);
    }
}
