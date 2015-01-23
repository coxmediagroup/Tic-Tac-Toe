package com.ntsdev.game;

public class Board {
    private Cell [][] board = new Cell[3][3];

    public Board(){
        initializeBoard();
    }

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

    public CellState getState(int x, int y){
        return board[x][y].getState();
    }

    public void setState(int x, int y, CellState state){
        board[x][y].setState(state);
    }

    public boolean cellAvailable(int x, int y){
        return board[x][y].getState() == CellState.BLANK;
    }
    
    public CellState checkWinner(){
        if(checkWin(CellState.X)) return CellState.X;
        if(checkWin(CellState.O)) return CellState.O;
        return CellState.BLANK;
    }

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

    private void initializeBoard(){
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                board[i][j] = new Cell();
            }
        }
    }

    public boolean checkWin(CellState playerState){
        //if any combination wins, return true
        for(int i=0;i<3;i++){
            if(checkHorizontal(i, playerState)) return true;
            if(checkVertical(i, playerState)) return true;
        }
        return checkDiagonals(playerState);
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
