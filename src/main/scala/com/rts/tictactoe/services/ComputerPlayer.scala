package com.rts.tictactoe.services;

import org.scalatra._
import scalate.ScalateSupport
import com.rts.tictactoe.models.GameBoard
import com.rts.tictactoe.models.GameBoardMinMax

class ComputerPlayer extends ScalatraServlet with ScalateSupport {
  
  get("/nextMove/:boardSquares") {
   
    val boardSquaresArray: Array[String] = {
      if ({params("boardSquares")}.last == ',')
        {params("boardSquares")}.split(",") ++ Array(" ");
      else
        {params("boardSquares")}.split(",");
    }
    
    val gameBoard = new GameBoardMinMax(boardSquaresArray, false);
    Ok(gameBoard.bestMove);    
  }

}
