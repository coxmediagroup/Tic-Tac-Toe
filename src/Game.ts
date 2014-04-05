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
				for(var i=0; i<this._winningSequences.length; i++) {
					var match1 = this._humanPlayerPlayedMoves.indexOf(this._winningSequences[i][0]);
					var match2 = this._humanPlayerPlayedMoves.indexOf(this._winningSequences[i][1]);
					var match3 = this._humanPlayerPlayedMoves.indexOf(this._winningSequences[i][2]);
					if(match1 !== -1 && match2 !== -1 && match3 !== -1) {
						console.log('Winner is Human Player.');
						return this._winner = 'Human Player';
					}
				}
			}
			
			// check if computer player has played at least three moves
			if(this._computerPlayerPlayedMoves.length >= 3) {
				// check if computer won (should always happen)
				for(var i=0; i<this._winningSequences.length; i++) {
					var match1 = this._computerPlayerPlayedMoves.indexOf(this._winningSequences[i][0]);
					var match2 = this._computerPlayerPlayedMoves.indexOf(this._winningSequences[i][1]);
					var match3 = this._computerPlayerPlayedMoves.indexOf(this._winningSequences[i][2]);
					if(match1 !== -1 && match2 !== -1 && match3 !== -1) {
						console.log('Winner is Computer Player.');
						return this._winner = 'Computer Player';
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