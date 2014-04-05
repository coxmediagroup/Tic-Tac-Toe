/// <reference path="IObserver.ts" /> 
module TicTacToe {
	export class Game implements IObserver {
		constructor() {}

	    update(arg:any) {
	        console.log('Game has been notified and ' + arg.player + ' made move at position #' + arg.madeMove);
	    }
	}
}