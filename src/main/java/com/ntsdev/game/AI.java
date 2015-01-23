package com.ntsdev.game;

public class AI {

    private final CellState computerState = CellState.X;
    private final CellState playerState = CellState.O;

    //computer always makes winning move

    public boolean isWinningMove(int x, int y, Board board, CellState stateToCheck){
        Board copy = board.copy();
        copy.setState(x,y,stateToCheck);
        return checkWin(copy, stateToCheck);
    }

    private boolean checkWin(Board board, CellState state){
        //if any combination wins, return true
        for(int i=0;i<3;i++){
            if(checkHorizontal(board, i, state)) return true;
            if(checkVertical(board, i, state)) return true;
        }
        return checkDiagonals(board, state);
    }

    private boolean checkHorizontal(Board board, int row, CellState state){
        for(int i=0;i<3;i++){
            CellState cellState = board.getState(row, i);
            boolean match = (cellState == state);
            if(!match){
                return false;
            }
        }
        return true;
    }

    private boolean checkVertical(Board board, int col, CellState state){
        for(int i=0;i<3;i++){
            CellState cellState = board.getState(i, col);
            boolean match = (cellState == state);
            if(!match){
                return false;
            }
        }
        return true;
    }

    private boolean checkDiagonals(Board board, CellState state){
        return
        //top left to bottom right
        ((board.getState(0,0) == state) &&
        (board.getState(1,1) == state) &&
        (board.getState(2,2) == state)) ||

        //top right to bottom left
        ((board.getState(0,2) == state) &&
        (board.getState(1,1) == state) &&
        (board.getState(2,0) == state));
    }

}
