package com.ntsdev.game;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * The computer AI for Tic-Tac-Toe.  Implemented using the minimax algorithm to guarantee a computer win
 * or draw.
 */
public class AI {
    private final CellState computerPlayer = CellState.X;
    private final CellState humanPlayer = CellState.O;

    private List<Result> results = new ArrayList<>(); //stores calculated moves for the computer

    /**
     * A result including a score (relative value of a move toward a win) and a move (position)
     */
    class Result {
        private int score;
        private Position position;

        Result(int score, Position position) {
            this.score = score;
            this.position = position;
        }

        public String toString() {
            return "Score: [" + score + "] Position: x[" + position.getX() + "] y[" + position.getY() + "]";
        }

    }

    /**
     * The computer makes a move
     *
     * @param board the current game board
     * @return the board with the computer's move applied
     */
    public Board makeMove(Board board) {
        results.clear();

        int score = minimax(computerPlayer, board.copy(), 0);
        Position move = getBestMove(score);

        board.makeMove(move, computerPlayer);
        return board;
    }

    /**
     * Finds the best calculated move for the computer
     *
     * @param bestScore the calculated score of the move
     * @return the best move
     */
    Position getBestMove(int bestScore) {
        Result best = null;
        for (Result result : results) {
            if (result.score == bestScore) {
                best = result;
                break;
            }
        }
        return best.position;
    }

    int calcMin(List<Integer> list) {
        return Collections.min(list);
    }

    int calcMax(List<Integer> list) {
        return Collections.max(list);
    }

    /**
     * Implementation of minimax algorithm to minimize chance of winning with the human player's moves and maximize the
     * chance of winning by the computer's moves.  Used to select the best move for the computer to make.
     * reference: http://en.wikipedia.org/wiki/Minimax
     *
     * @param player which player's moves should be calculated
     * @param board  the game board
     * @param depth  recursion depth (depth of game search tree)
     * @return the best score for the computer
     */
    private int minimax(CellState player, Board board, int depth) {
        List<Integer> scores = new ArrayList<>();
        List<Position> moves = board.getAvailableMoves();

        if (board.checkWin(computerPlayer)) return 1;
        if (board.checkWin(humanPlayer)) return -1;
        if (moves.isEmpty()) return 0;

        for (Position move : moves) {
            board.makeMove(move, player); //make the move for the player
            if (player == computerPlayer) {
                int currentScore = minimax(humanPlayer, board, depth + 1);
                scores.add(currentScore);
                if (depth == 0) {
                    results.add(new Result(currentScore, move));
                }
            } else {
                int currentScore = minimax(computerPlayer, board, depth + 1);
                scores.add(currentScore);
            }
            board.makeMove(move, CellState.BLANK); //undo move
        }

        if (player == computerPlayer) {
            return calcMax(scores); //maximize computer score
        } else {
            return calcMin(scores); //minimize user score
        }
    }

}
