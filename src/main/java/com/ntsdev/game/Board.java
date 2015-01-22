package com.ntsdev.game;

public class Board {
    private Cell [][] board = new Cell[3][3];

    public Board(){
        initializeBoard();
    }

    public boolean makeMove(int x, int y, CellState state){
        boolean success = false;

        CellState currentState = board[x][y].getState();
        switch(currentState){
            case BLANK:
                board[x][y].setState(state);
                success = true;
                break;
            case X:
                success = false;
                break;
            case O:
                success = false;
                break;
        }

        return success;
    }

    public CellState getState(int x, int y){
        return board[x][y].getState();
    }

    private void initializeBoard(){
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                board[i][j] = new Cell();
            }
        }
    }
}
