package com.rts.tictactoe.services;

import org.scalatra._
import scalate.ScalateSupport
import com.rts.tictactoe.models.GameBoard

class ComputerPlayer extends ScalatraServlet with ScalateSupport {
  
  get("/nextMove/:boardSquares") {
   
    val boardSquaresArray: Array[String] = {
      if ({params("boardSquares")}.last == ',')
        {params("boardSquares")}.split(",") ++ Array(" ");
      else
        {params("boardSquares")}.split(",");
    }
    
    val gameBoard = new GameBoard(boardSquaresArray);
    Ok(ComputerPlayer.nextComputerMove(gameBoard));    
  }

}
object ComputerPlayer {
  
  private val COMPUTER_SYMBOL = "O";
  private val PLAYER_SYMBOL = "X";
  
  def nextComputerMove(gameBoard:GameBoard):Int = {
    val winningComputerMove = gameBoard.winningMoveFor(COMPUTER_SYMBOL); 
    lazy val winningPlayerMove = gameBoard.winningMoveFor(PLAYER_SYMBOL);
    
    if (winningComputerMove != -1) 
      winningComputerMove;
    else if (winningPlayerMove != -1) 
      winningPlayerMove;
    else {
      if (gameBoard.futureWinningMoveExistsFor(PLAYER_SYMBOL)) {
        gameBoard.bestSquareToBlockWinningScenarioFor(PLAYER_SYMBOL);
      } else {
        gameBoard.highestPrioritySquareOpen();
      }
    }
  }
  
}
