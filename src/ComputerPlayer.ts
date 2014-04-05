/// <reference path="Player.ts" />
/// <reference path="IObserver.ts" /> 
module TicTacToe { 
	export class ComputerPlayer extends Player implements IObserver {
		constructor() { super("Computer Player"); }

		makeMove(boardIndex?:number) {
			if(typeof boardIndex == "number") {
				super.makeMove(boardIndex); 
			} else {
				console.log(this.getLabel() + ' is using their wits...');
				var calculatedMove:number = 999;
				super.makeMove(calculatedMove);
				return calculatedMove;
			}
		}

		update(arg:any) {
	        console.log('Computer player has been notified and ' + arg.player + ' made move at position #' + arg.madeMove);
	    }
	}
}