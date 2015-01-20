package com.rts.tictactoe.models

class GameBoard(val boardSquaresArray:Array[String]) {

  lazy val middleSquareSymbol = boardSquaresArray(4);
  lazy val filledSquaresCount = boardSquaresArray.filter { x => x != " " }.size
  
  def symbolWinsWith(winningCombination:List[Int], symbol: String):Boolean = winningCombination.filter { x => boardSquaresArray(x) == symbol }.length == 3;
  
  def playerWinsWith(winningCombination:List[Int]):Boolean = if (symbolWinsWith(winningCombination, "X") || symbolWinsWith(winningCombination, "O")) true else false;   

  def winningCombination():Option[List[Int]] = GameBoard.winningCombinationsList.find { x => playerWinsWith(x) };
  
  def highestPrioritySquareOpen():Int = {
    val prioritizedListOfRemainingSquares = GameBoard.squarePrioritization.filter { x => boardSquaresArray(x) == " " };
    if (prioritizedListOfRemainingSquares.isEmpty)
      return -1;
    else
      return prioritizedListOfRemainingSquares.head;
  };

  //TODO: Research a way to not have to re-execute the winningSquareFor method when the winning combination found
  def winningMoveFor(symbol: String):Int = {   
    val winningCombination = GameBoard.winningCombinationsList.find { x => winningSquareFor(symbol, x) != -1 }
    if (winningCombination == None) 
      return -1;
    else
      return winningSquareFor(symbol, winningCombination.get)
  }
  
  //Returns the square to be played in order to win the game, or -1 if there is no winning move possible
  def winningSquareFor(symbol: String, winningCombination: List[Int]):Int = {
    val opposingSymbol = if (symbol=="O") "X" else "O";
    val ownedOrAvailableSquaresInWinningCombination = winningCombination.filter { x => boardSquaresArray(x) != opposingSymbol }
    
    if (ownedOrAvailableSquaresInWinningCombination.length < 3)
      return -1;
    else {
      val availableSquaresInWinningCombination = ownedOrAvailableSquaresInWinningCombination.filter { x => boardSquaresArray(x) == " "};
      if (availableSquaresInWinningCombination.length == 1) 
        return availableSquaresInWinningCombination.head 
      else 
        return -1;
    }
  }
  
  def futureWinningMoveExistsFor(symbol: String):Boolean = middleSquareSymbol == GameBoard.opposingSymbol(symbol) && filledSquaresCount == 3
  def bestSquareToBlockWinningScenarioFor(symbol: String) = 1;
}
object GameBoard {
  
  def opposingSymbol(symbol: String) = if (symbol == "O") "X" else "O";
  
  //Ordered array of square indices in order of best squares to play in
  def squarePrioritization: List[Int] = List(4, 0, 2, 6, 8, 1, 3, 5, 7);

  def winningCombinationsList: List[List[Int]] = 
    List(List(0,1,2),
        List(3,4,5),
        List(6,7,8),
        List(0,3,6),
        List(1,4,7),
        List(2,5,8),
        List(0,4,8),
        List(2,4,6));
  
}