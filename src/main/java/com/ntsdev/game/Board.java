package com.ntsdev.game;

/**
 * The Tic-Tac-Toe game board
 */
public class Board {
    private Cell [][] board = new Cell[3][3];

    public Board(){
        initializeBoard();
    }

    /**
     * Attempts to make a move on the board
     * @param x x coordinate on the game board
     * @param y y coordinate on the game board
     * @param state either an X or an O
     * @return true if the move could be made
     */
    public boolean makeMove(int x, int y, CellState state){
        boolean success;
        if(cellAvailable(x,y)){
            board[x][y].setState(state);
            success = true;
        }
        else{
            success = false;
        }
        return success;
    }

    /**
     * Gets the state of a cell on the game board
     * @param x x coordinate of the game board
     * @param y y coordinate of the game board
     * @return the current state of the given cell
     */
    public CellState getState(int x, int y){
        return board[x][y].getState();
    }

    /**
     * Sets the state of a cell on the game board
     * @param x x coordinate of the game board
     * @param y y coordinate of the game board
     * @param state the state to set
     */
    public void setState(int x, int y, CellState state){
        board[x][y].setState(state);
    }

    /**
     * Checks if a letter has already been placed on the game board
     * @param x x coordinate of the game board
     * @param y y coordinate of the game board
     * @return true if the cell is blank
     */
    public boolean cellAvailable(int x, int y){
        return board[x][y].getState() == CellState.BLANK;
    }

    /**
     * Checks if the board is full with no winner
     * @return true if the game is a draw
     */
    public boolean draw(){
        if(!checkWin(CellState.X) && !checkWin(CellState.O)){
            for(int i=0;i<3;i++){
                for(int j=0;j<3;j++){
                    if(getState(i,j) == CellState.BLANK){
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
                copy.setState(x,y, state);
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
        boardString.append("{\"board\":[");
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
            boardString.append("]");
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

    private void initializeBoard(){
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                board[i][j] = new Cell();
            }
        }
    }

    private boolean checkHorizontal(int row, CellState state){
        for(int i=0;i<3;i++){
            CellState cellState = getState(row, i);
            boolean match = (cellState == state);
            if(!match){
                return false;
            }
        }
        return true;
    }

    private boolean checkVertical(int col, CellState state){
        for(int i=0;i<3;i++){
            CellState cellState = getState(i, col);
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
                ((getState(0,0) == state) &&
                        (getState(1,1) == state) &&
                        (getState(2,2) == state)) ||

                        //top right to bottom left
                        ((getState(0,2) == state) &&
                                (getState(1,1) == state) &&
                                (getState(2, 0) == state));
    }

}
