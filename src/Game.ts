/// <reference path="IObserver.ts" /> 
/// <reference path="PositionPrettyName.ts" /> 
module TicTacToe {
	export class Game implements IObserver {

		private _computerPlayerPlayedMoves:number[] = [];
		private _humanPlayerPlayedMoves:number[] = [];
		private _winner:any = false;
		private _winningSequences = [
			[0,1,2],
			[3,4,5],
			[6,7,8],
			[0,3,6],
			[1,4,7],
			[2,5,8],
			[0,5,8],
			[2,5,6]
		];

		private _checkForWinner() {

		}

		getWinner() {
			return this._winner;
		}

	    update(arg:any) {
	        console.log(
	        	'Game has been notified and ' 
	        	+ arg.player 
	        	+ ' made move at position #' 
	        	+ arg.madeMove 
	        	+ ' aka ' 
	        	+ PositionPrettyName[arg.madeMove]
        	);

        	if(arg.player === 'Computer Player') {
        		this._computerPlayerPlayedMoves.push(arg.madeMove);
        	} else {
        		this._humanPlayerPlayedMoves.push(arg.madeMove);
        	}

        	this._checkForWinner();
	    }

	}
}