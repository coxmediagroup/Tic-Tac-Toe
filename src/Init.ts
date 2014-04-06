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

		humanPlayer.makeMove(0);
	}
}

TicTacToe.init();