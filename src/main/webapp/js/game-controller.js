'use strict';

angular.module('app').controller("GameController", function(gameBoard, ComputerPlayerService, WinnerService){
    var gameController = this;
    gameController.title = "Tic Tac Toe";
    gameController.grid = new Array(3);
    gameController.boardDisabled = false;
    gameController.gameOver = false;
    gameController.gameWon = false;
    
    gameController.makePlayerMove = function(row, col) {
    	//only process the event if it is the players turn
    	if (!gameController.boardDisabled && !gameController.gameWon && !gameBoard.isFull()) {
    		gameController.boardDisabled = true;
    		gameBoard.setSquare(row, col, 'X');	
    		gameController.checkForWinner(true);
    	}
    }
    
    gameController.completePlayerMove = function() {
 		if (gameController.gameWon || gameBoard.isFull()) {
  		 	gameController.gameOver = true;
 		} else { 
			gameController.makeComputerMove();
    	}   	
    }
    
    gameController.makeComputerMove = function() {
		ComputerPlayerService.nextMove(gameBoard.squares).then(function() {
			gameController.placeComputerMoveOnBoard(ComputerPlayerService.computerNextMoveIndex());    		    
		}, function(reason) {
			alert(reason);
		});
    }
    
    gameController.placeComputerMoveOnBoard = function(squareIndex) {
 		gameBoard.setSquareByIndex(ComputerPlayerService.computerNextMoveIndex(), 'O');
 		gameController.checkForWinner(false);
    }
    
    gameController.completeComputerMove = function() {
 		
     	if (gameController.gameWon || gameBoard.isFull()) {
   		 	gameController.gameOver = true;
     	} else {     		 
	    	gameController.boardDisabled = false; 
		}    
    }
    
    gameController.checkForWinner = function(playerJustMoved) {
		WinnerService.winningCombination(gameBoard.squares).then(function() {
			gameBoard.winningCombination = WinnerService.theWinningCombination();
			if (gameBoard.winningCombination[0] != -1) {
				gameController.gameWon = true;
			}
			
			if (playerJustMoved) 
				gameController.completePlayerMove();
			else
				gameController.completeComputerMove(); 
		}); 
    }
    
    gameController.getSquareSymbol = function(row, col) {
    	return gameBoard.getSquareSymbol(row,col);
    }
    
    gameController.isWinningSquare = function(row, col) {
    	return gameBoard.isWinningSquare(row, col);
    }
    
});