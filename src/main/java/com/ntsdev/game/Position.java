package com.ntsdev.game;

public class Position {
    private int x, y;

    private static Position [] possiblePositions = {
            new Position(0,0), new Position(0,1), new Position(0,2),
            new Position(1,0), new Position(1,1), new Position(1,2),
            new Position(2,0), new Position(2,1), new Position(2,2)
    };

    public static Position withCoordinates(int x, int y){
        for(Position position: possiblePositions){
            if(position.getX() == x && position.getY() == y){
                return position;
            }
        }
        throw new IllegalArgumentException("Invalid position for values x: [" + x + "] y: [" + y + "]");
    }

    public Position(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

}
