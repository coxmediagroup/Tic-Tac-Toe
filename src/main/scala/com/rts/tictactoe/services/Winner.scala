package com.rts.tictactoe.services

import org.scalatra._
import scalate.ScalateSupport
import com.rts.tictactoe.models.GameBoardMinMax

class Winner extends ScalatraServlet with ScalateSupport {

    get("/winningCombination/:boardSquares") {

      val boardSquaresArray: Array[String] = {
        if ({params("boardSquares")}.last == ',')
          {params("boardSquares")}.split(",") ++ Array(" ");
        else
          {params("boardSquares")}.split(",");
      }
      
      val gameBoard = new GameBoardMinMax(boardSquaresArray, true);
      val winningCombination = gameBoard.winningCombination;
      
      if (winningCombination.isEmpty)
        Ok("-1,-1,-1");
      else
        Ok(winningCombination.mkString(","));
    }

}