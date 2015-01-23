package com.ntsdev.api;

import com.ntsdev.game.AI;
import com.ntsdev.game.Board;
import com.ntsdev.game.CellState;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

@RestController
@RequestMapping("/api")
public class ApiController {

    private AI ai = new AI();
    //this is actually OK to share across clients...it's stateless

    @RequestMapping("/newgame")
    public String newGame(HttpSession session, HttpServletResponse response) {
        Board board = new Board();
        session.setAttribute("board", board);
        response.setContentType("application/json");
        return board.toJSON();
    }

    @RequestMapping("/board")
    @ResponseBody
    public String gameBoard(HttpSession session) {
        Object maybeBoard = session.getAttribute("board");
        if(maybeBoard == null){
            Board newBoard = new Board();
            session.setAttribute("board", newBoard);
            return newBoard.toJSON();
        }
        else{
            Board board = (Board) maybeBoard;
            return board.toJSON();
        }
    }

    @RequestMapping("/makemove")
    @ResponseBody
    public String playerMove(
            HttpSession session,
            @RequestParam("x") Integer x,
            @RequestParam("y") Integer y,
            HttpServletResponse response) throws IOException {

        Board board = (Board) session.getAttribute("board");
        board.makeMove(x,y, CellState.O); //player is always "o"
        if(board.checkWin(CellState.O)){
            response.sendRedirect("/winner.html");
        }

        board = ai.makeMove(board);
        session.setAttribute("board", board);

        if(board.checkWin(CellState.X)){
            response.sendRedirect("/loser.html");
        }

        return board.toJSON();
    }

}
