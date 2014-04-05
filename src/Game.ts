/// <reference path="IObserver.ts" /> 
/// <reference path="PositionPrettyName.ts" /> 
module TicTacToe {
	export class Game implements IObserver {

		players:any[] = [];


	    update(arg:any) {
	        console.log(
	        	'Game has been notified and ' 
	        	+ arg.player 
	        	+ ' made move at position #' 
	        	+ arg.madeMove 
	        	+ ' aka ' 
	        	+ PositionPrettyName[arg.madeMove]
        	);
	    }
	}
}