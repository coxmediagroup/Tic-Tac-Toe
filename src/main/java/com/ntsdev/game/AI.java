package com.ntsdev.game;

import java.util.List;

public class AI {

    private final CellState computerPlayer = CellState.X;
    private final CellState humanPlayer = CellState.O;

    class Result {
        private int score;
        private Position position;

        Result(int score, Position position) {
            this.score = score;
            this.position = position;
        }

        public String toString(){
            return "Score: [" + score + "] Position: x[" + position.getX() + "] y[" + position.getY() + "]";
        }
    }

    /**
     * The computer makes a move
     * @param board the current game board
     * @return the board with the computer's move applied
     */
    public Board makeMove(Board board){
        Result result = minimax(computerPlayer, board.copy(), 0);
        System.out.println(result);
        board.makeMove(result.position, computerPlayer);
        return board;
    }

    private Result minimax(CellState player, Board board, int depth){
        List<Position> moves = board.getAvailableMoves();

        int bestX = -1;
        int bestY = -1;
        int currentScore;
        int bestScore;

        if(player == computerPlayer){
            bestScore = Integer.MIN_VALUE;
        }
        else{
            bestScore = Integer.MAX_VALUE;
        }

        if(moves.isEmpty() || board.checkWin(computerPlayer) || board.checkWin(humanPlayer)){  //game over
            bestScore = evaluate(board);
        }
        else{
            for(Position move: moves){
                board.makeMove(move, player); //make the move for the player
                if(player == computerPlayer){ //maximize score for computer
                    Result result = minimax(humanPlayer, board, depth + 1);
                    currentScore = result.score;
                    if(currentScore > bestScore){
                        bestScore = currentScore;
                        Position position = result.position;
                        bestX = position.getX();
                        bestY = position.getY();
                    }
                    if(currentScore == 1) {
                        System.out.println("COMPUTER WINS!");
                        return new Result(bestScore, Position.withCoordinates(bestX, bestY));
                    }
                }
                else{ //minimize score for player
                    Result result = minimax(computerPlayer, board, depth + 1);
                    currentScore = result.score;
                    if(currentScore < bestScore){
                        bestScore = currentScore;
                        Position position = result.position;
                        bestX = position.getX();
                        bestY = position.getY();
                    }
                }
                board.makeMove(move, CellState.BLANK);
            }
            return new Result(bestScore, Position.withCoordinates(bestX, bestY));
        }

        System.out.println("bestX: " + bestX + " bestY: " + bestY + " bestScore: " + bestScore);
        return new Result(bestScore, Position.withCoordinates(bestX, bestY));
    }

    private int evaluate(Board board){
        CellState winner = board.checkWinner();
        if(winner == computerPlayer){
            System.out.println(board);
            return 1;
        }
        else if(winner == humanPlayer){
            return -1;
        }
        else{
            return 0;
        }
    }

}
