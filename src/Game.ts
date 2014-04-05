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

			// check if human player has played at least three moves
			if(this._humanPlayerPlayedMoves.length >= 3) {
				// check if human won (should never happen)
				for(var i=0,j=1,k=2; k<this._humanPlayerPlayedMoves.length; i++,j++,k++) {
					for(var l=0; l<this._winningSequences.length; l++) {
						var match1 = this._winningSequences[l].indexOf(this._humanPlayerPlayedMoves[i]);
						var match2 = this._winningSequences[l].indexOf(this._humanPlayerPlayedMoves[j]);
						var match3 = this._winningSequences[l].indexOf(this._humanPlayerPlayedMoves[k]);
						if(match1 !== -1 && match2 !== -1 && match3 !== -1) {
							return this._winner = 'Human Player';
						}
					}
				}
			// check if computer player has played at least three moves
			} else if(this._computerPlayerPlayedMoves.length >= 3) {
				// check if computer won (should always happen)
				for(var i=0,j=1,k=2; k<this._computerPlayerPlayedMoves.length; i++,j++,k++) {
					for(var l=0; l<this._winningSequences.length; l++) {
						var match1 = this._winningSequences[l].indexOf(this._computerPlayerPlayedMoves[i]);
						var match2 = this._winningSequences[l].indexOf(this._computerPlayerPlayedMoves[j]);
						var match3 = this._winningSequences[l].indexOf(this._computerPlayerPlayedMoves[k]);
						if(match1 !== -1 && match2 !== -1 && match3 !== -1) {
							return this._winner = 'Computer Player';
						}
					}
				}
			}
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