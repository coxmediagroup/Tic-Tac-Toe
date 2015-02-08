package com.ntsdev.game;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * The Tic-Tac-Toe game board
 */
public class Board {
    private Cell[][] board = new Cell[3][3];

    List<List<Position>> winningCombinations = initializeWinningCombinations();

    public Board(){
        initializeBoard();
    }

    /**
     * Attempts to make a move on the board
     * @param position coordinates for the move
     * @param state either an X or an O
     * @return true if the move could be made
     */
    public boolean makeMove(Position position, CellState state){
        boolean success;
        if(cellAvailable(position) || state == CellState.BLANK){
            board[position.getX()][position.getY()].setState(state);
            success = true;
        }
        else{
            success = false;
        }
        return success;
    }

    /**
     * Gets the state of a cell on the game board
     * @param position Position to check
     * @return the current state of the given cell
     */
    public CellState getState(Position position){
        return board[position.getX()][position.getY()].getState();
    }

    /**
     * Sets the state of a cell on the game board
     * @param position Position to check
     * @param state the state to set
     */
    public void setState(Position position, CellState state){
        board[position.getX()][position.getY()].setState(state);
    }

    /**
     * Checks if a letter has already been placed on the game board
     * @param position Position to check
     * @return true if the cell is blank
     */
    public boolean cellAvailable(Position position){
        return board[position.getX()][position.getY()].getState() == CellState.BLANK;
    }

    /**
     * Checks if the board is full with no winner
     * @return true if the game is a draw
     */
    public boolean draw(){
        if(!checkWin(CellState.X) && !checkWin(CellState.O)){
            for(int i=0;i<3;i++){
                for(int j=0;j<3;j++){
                    if(getState(Position.withCoordinates(i,j)) == CellState.BLANK){
                        return false;
                    }
                }
            }
        }
        return true;
    }


    /**
     * Makes a deep copy of the game board
     * @return a copy of the current board
     */
    public Board copy(){
        Board copy = new Board();
        for(int x=0;x<3;x++){
            for(int y=0;y<3;y++){
                CellState state = board[x][y].getState();
                copy.setState(Position.withCoordinates(x,y), state);
            }
        }
        return copy;
    }

    /**
     * Returns a JSON representation of the board
     * @return a JSON String of the game board
     */
    public String toJSON(){
        /*
           {
            "board" :
                [
                 ["X","X","_"],
                 ["O","X","_"],
                 ["X","0","X"]
                ]
            }
         */
        StringBuilder boardString = new StringBuilder(256);
        boardString.append("{\"board\":[\n");
        for(int i=0;i<3;i++){
            boardString.append("[");
            for(int j=0;j<3;j++){
                boardString.append('\"');
                boardString.append(board[i][j]);
                boardString.append('\"');
                if(j<2){
                    boardString.append(",");
                }
            }
            boardString.append("]\n");
            if(i<2) {
                boardString.append(',');
            }
        }
        boardString.append("]}");

        return boardString.toString();
    }

    /**
     * Checks if the given CellState (X or O) has won
     * @param playerState the state to check
     * @return true if the playerState is a winner
     */
    public boolean checkWin(CellState playerState){
        //if any combination wins, return true
        for(int i=0;i<3;i++){
            if(checkHorizontal(i, playerState)) return true;
            if(checkVertical(i, playerState)) return true;
        }
        return checkDiagonals(playerState);
    }

    /**
     * Returns either X or O if there is a winner
     * @return X or O if there is a winner, BLANK otherwise
     */
    public CellState checkWinner(){
        if(checkWin(CellState.X)) return CellState.X;
        if(checkWin(CellState.O)) return CellState.O;
        return CellState.BLANK;
    }

    /**
     * Returns all available moves
     * @return
     */
    public List<Position> getAvailableMoves(){
        List<Position> availableMoves = new ArrayList<>();

        CellState potentialWinner = checkWinner();
        if(potentialWinner == CellState.X || potentialWinner == CellState.O){
            return availableMoves;
        }

        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                Position position = Position.withCoordinates(i,j);
                if(cellAvailable(position)){
                    availableMoves.add(position);
                }
            }
        }
        return availableMoves;
    }

    @Override
    public String toString(){
        return toJSON();
    }

    private void initializeBoard(){
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                board[i][j] = new Cell();
            }
        }
    }

    private boolean checkHorizontal(int row, CellState state){
        for(int i=0;i<3;i++){
            CellState cellState = getState(Position.withCoordinates(row, i));
            boolean match = (cellState == state);
            if(!match){
                return false;
            }
        }
        return true;
    }

    private boolean checkVertical(int col, CellState state){
        for(int i=0;i<3;i++){
            CellState cellState = getState(Position.withCoordinates(i, col));
            boolean match = (cellState == state);
            if(!match){
                return false;
            }
        }
        return true;
    }

    private boolean checkDiagonals(CellState state){
        return
                //top left to bottom right
                ((getState(Position.withCoordinates(0,0)) == state) &&
                        (getState(Position.withCoordinates(1,1)) == state) &&
                        (getState(Position.withCoordinates(2,2)) == state)) ||

                        //top right to bottom left
                        ((getState(Position.withCoordinates(0,2)) == state) &&
                                (getState(Position.withCoordinates(1,1)) == state) &&
                                (getState(Position.withCoordinates(2, 0)) == state));
    }

    private List<List<Position>> initializeWinningCombinations(){
        List<Position> horizontalFirstRow = Arrays.asList(
                Position.withCoordinates(0,0), Position.withCoordinates(0,1), Position.withCoordinates(0,2));
        List<Position> horizontalSecondRow = Arrays.asList(
                Position.withCoordinates(1,0), Position.withCoordinates(1,1), Position.withCoordinates(1,2));
        List<Position> horizontalThirdRow = Arrays.asList(
                Position.withCoordinates(2,0), Position.withCoordinates(2,1), Position.withCoordinates(2,2));
        List<Position> verticalFirstColumn = Arrays.asList(
                Position.withCoordinates(0,0), Position.withCoordinates(1,0), Position.withCoordinates(2,0));
        List<Position> verticalSecondColumn = Arrays.asList(
                Position.withCoordinates(0,1), Position.withCoordinates(1,1), Position.withCoordinates(2,1));
        List<Position> verticalThirdColumn = Arrays.asList(
                Position.withCoordinates(0,2), Position.withCoordinates(1,2), Position.withCoordinates(2,2));
        List<Position> diagonalLeftToRight = Arrays.asList(
                Position.withCoordinates(0,0), Position.withCoordinates(1,1), Position.withCoordinates(2,2));
        List<Position> diagonalRightToLeft = Arrays.asList(
                Position.withCoordinates(0,2), Position.withCoordinates(1,1), Position.withCoordinates(2,0));

        return Arrays.asList(
                horizontalFirstRow, horizontalSecondRow, horizontalThirdRow, verticalFirstColumn,
                verticalSecondColumn, verticalThirdColumn, diagonalLeftToRight, diagonalRightToLeft);
    }

}
