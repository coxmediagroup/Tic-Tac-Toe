package com.ntsdev.game;

public class AI {

    private final CellState computerState = CellState.X;
    private final CellState playerState = CellState.O;

    public Board makeMove(Board board){
        //see if computer can win with this turn, or if player can win, move to that space
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                if(isWinningMove(i,j,board,computerState)){
                    board.makeMove(i,j,computerState);
                    return board;
                }
                else if(isWinningMove(i,j,board,playerState)){
                    board.makeMove(i,j,computerState);
                    return board;
                }
            }
        }
        //nobody's going to win on this move, so try to get a corner or the center
        if(couldPlayCorner(board)) return board;
        if(couldPlayCenter(board)) return board;

        //just pick somewhere
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++) {
                if(board.cellAvailable(i,j)){
                    board.makeMove(i,j,computerState);
                    return board;
                }
            }
        }

        return board; //shouldn't happen
    }

    public boolean isWinningMove(int x, int y, Board board, CellState stateToCheck){
        Board copy = board.copy();
        copy.setState(x,y,stateToCheck);
        return copy.checkWin(stateToCheck);
    }


    private boolean couldPlayCorner(Board board){
        boolean couldPlay = false;
        if(board.cellAvailable(0,0)){
            board.makeMove(0,0,computerState);
            couldPlay = true;
        }
        else if(board.cellAvailable(0,2)){
            board.makeMove(0,2,computerState);
            couldPlay = true;
        }
        else if(board.cellAvailable(2,2)){
            board.makeMove(2,2,computerState);
            couldPlay = true;
        }
        else if(board.cellAvailable(2,0)){
            board.makeMove(2,0,computerState);
            couldPlay = true;
        }
        return couldPlay;
    }

    private boolean couldPlayCenter(Board board){
        boolean couldPlay = false;
        if(board.cellAvailable(1,1)){
            board.makeMove(1,1,computerState);
            couldPlay = true;
        }
        return couldPlay;
    }

}
