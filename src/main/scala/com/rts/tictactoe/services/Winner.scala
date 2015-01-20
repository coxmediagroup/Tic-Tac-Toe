package com.rts.tictactoe.services

import org.scalatra._
import scalate.ScalateSupport
import com.rts.tictactoe.models.GameBoard

class Winner extends ScalatraServlet with ScalateSupport {

    get("/winningCombination/:boardSquares") {

      val boardSquaresArray: Array[String] = {
        if ({params("boardSquares")}.last == ',')
          {params("boardSquares")}.split(",") ++ Array(" ");
        else
          {params("boardSquares")}.split(",");
      }
      
      val gameBoard = new GameBoard(boardSquaresArray);
      val winningCombination = gameBoard.winningCombination();
      
      if (winningCombination.isDefined)
        Ok(winningCombination.get.mkString(","));
      else
        Ok("-1,-1,-1");
    }

}