/// <reference path="Game.ts" />
/// <reference path="Board.ts" />
/// <reference path="Player.ts" />
/// <reference path="ComputerPlayer.ts" />
/// <reference path="HumanPlayer.ts" />
module TicTacToe {
	export function init() {
		var game = new TicTacToe.Game();
		var humanPlayer = new TicTacToe.HumanPlayer();
		var computerPlayer = new TicTacToe.ComputerPlayer();
		var board = new TicTacToe.Board(); 
		humanPlayer.registerObserver(game);
		humanPlayer.registerObserver(computerPlayer);
		computerPlayer.registerObserver(game);
		game.registerObserver(board); 
		game.registerObserver(computerPlayer);
		

		var cellClassName = document.getElementsByClassName("cell");
	   	var cellClickHandler = function() {
	       var played = this.getAttribute("played");
	       if(played === 'true') {
	       	alert('Position has already been played.');
	       } else {
	       	humanPlayer.makeMove(parseInt(this.getAttribute("cellIndex"), 10));
	       	computerPlayer.makeMove();
	       }
	    };

	    for(var i=0;i<cellClassName.length;i++){
	      cellClassName[i].addEventListener('click', cellClickHandler, false);
	    }

	}
}

TicTacToe.init();