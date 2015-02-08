package com.ntsdev.api;

import com.ntsdev.game.AI;
import com.ntsdev.game.Board;
import com.ntsdev.game.CellState;
import com.ntsdev.game.Position;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpSession;
import java.io.IOException;

@RestController
@RequestMapping("/api")
public class ApiController {

    @RequestMapping(value = "/newgame", method = RequestMethod.POST)
    public String newGame(HttpSession session) {
        Board board = new Board();
        session.setAttribute("board", board);
        return board.toJSON();
    }

    @RequestMapping("/board")
    public String gameBoard(HttpSession session) {
        Object maybeBoard = session.getAttribute("board");
        if (maybeBoard == null) {
            Board newBoard = new Board();
            session.setAttribute("board", newBoard);
            return newBoard.toJSON();
        } else {
            Board board = (Board) maybeBoard;
            return board.toJSON();
        }
    }

    @RequestMapping(value = "/makemove", method = RequestMethod.POST)
    public String playerMove(
            HttpSession session,
            @RequestParam("x") Integer x,
            @RequestParam("y") Integer y) throws IOException {

        Board board = (Board) session.getAttribute("board");
        board.makeMove(Position.withCoordinates(x, y), CellState.O); //player is always "o"

        if (!board.checkWin(CellState.O) && !board.getAvailableMoves().isEmpty()) {
            AI ai = new AI();
            board = ai.makeMove(board);
            session.setAttribute("board", board);
        }

        return board.toJSON();
    }

    @RequestMapping("/checkwin")
    public String checkWin(HttpSession session) {
        Board board = (Board) session.getAttribute("board");
        if (board.checkWin(CellState.O)) {
            return "You win!";
        } else if (board.checkWin(CellState.X)) {
            return "You lose!";
        } else if (board.draw()) {
            return "It's a draw!";
        }
        return "";
    }

}
