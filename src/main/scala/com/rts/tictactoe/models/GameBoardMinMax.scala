package com.rts.tictactoe.models

class GameBoardMinMax(val boardSquaresArray:Array[String], val isPlayerX:Boolean) {

  val boardValuesList:List[Int] = boardSquaresArray.toList.map { x => 
    if (x == "X") 
      1 
    else if (x == "O") 
      -1 
    else
      0;
    };
  
  val winningCombination = GameBoardMinMax.winningCombinationsList.filter { combination => 
      val combinationSum = combination.map { x => boardValuesList(x) }.sum;
      (combinationSum == 3 || combinationSum == -3)
  }
  
  lazy val availableMoves = boardValuesList.zipWithIndex map { case(squareValue, index) => if (squareValue != 0) -1 else index; } filter { x => x != -1 }

  val score = {
    
    if (winningCombination.isEmpty)
      0;
    else if (boardValuesList(winningCombination.head.head) == 1) 
      10;
    else
      -10;
  }
  
  def miniMax():Int = {
    if (score != 0 || (score == 0 && availableMoves.isEmpty)) {
      return score;
    }
    else {
        val scoresWithMoveIndex:List[(Int, Int)] = GameBoardMinMax.gameBoardsAfterNextMove(this).map { gameBoard =>  gameBoard.miniMax() }.zipWithIndex
        val bestMove = scoresWithMoveIndex.reduceLeft( (scoreIndexTuple1:(Int,Int), scoreIndexTuple2:(Int, Int)) => 
            if (isPlayerX) {
              if (scoreIndexTuple1._1 > scoreIndexTuple2._1) scoreIndexTuple1 else scoreIndexTuple2;
            } else {
              if (scoreIndexTuple1._1 < scoreIndexTuple2._1) scoreIndexTuple1 else scoreIndexTuple2;
            });
        return bestMove._1;
    }
  }
  
  def bestMove:Int = {
    val gameBoardsAfterNextMove:List[GameBoardMinMax] = GameBoardMinMax.gameBoardsAfterNextMove(this);
    val scoresWithMoveIndex:List[(Int, Int)] = gameBoardsAfterNextMove.map { gameBoard =>  gameBoard.miniMax() }.zipWithIndex
    val bestMove = scoresWithMoveIndex.reduceLeft( (scoreIndexTuple1:(Int,Int), scoreIndexTuple2:(Int, Int)) => 
        if (isPlayerX) {
          if (scoreIndexTuple1._1 > scoreIndexTuple2._1) scoreIndexTuple1 else scoreIndexTuple2;
        } else {
          if (scoreIndexTuple1._1 < scoreIndexTuple2._1) scoreIndexTuple1 else scoreIndexTuple2;
        });
    return availableMoves(bestMove._2);
  }
  
}
object GameBoardMinMax {
  
  def winningCombinationsList: List[List[Int]] = 
    List(List(0,1,2),
        List(3,4,5),
        List(6,7,8),
        List(0,3,6),
        List(1,4,7),
        List(2,5,8),
        List(0,4,8),
        List(2,4,6));
  
  def gameBoardsAfterNextMove(gameBoard:GameBoardMinMax):List[GameBoardMinMax] = {
      gameBoard.availableMoves.map { x => {
       val newBoardSquaresArray = gameBoard.boardSquaresArray.clone();
       newBoardSquaresArray.update(x, if (gameBoard.isPlayerX) "X" else "O");
       new GameBoardMinMax(newBoardSquaresArray, !gameBoard.isPlayerX)
      }}
  }

}