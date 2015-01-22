package com.ntsdev.game;

public class Cell {

    private CellState state = CellState.BLANK;

    public CellState getState(){
        return this.state;
    }

    public void setState(CellState state){
        this.state = state;
    }
}
