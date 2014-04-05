/// <reference path="Player.ts" />
/// <reference path="IObserver.ts" /> 
module TicTacToe { 
	export class ComputerPlayer extends Player implements IObserver {
		constructor() { super("Computer Player"); }

		private _computerPlayerPlayedMoves:number[] = [];
		private _humanPlayerPlayedMoves:number[] = [];
		private _aggregatePlayedMoves:number[] = [];

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

		// returns the next calculated move
		private _calculate():number {
			var nextMove:number;
			this._aggregatePlayedMoves = this._computerPlayerPlayedMoves.concat(this._humanPlayerPlayedMoves);
			if(typeof this._checkTwoInARow() === 'number') {
				nextMove = this._checkTwoInARow();
			}
			return nextMove;
		}

		// returns next move or false
		private _checkTwoInARow():any {
			var nextMove:any;

			if(this._computerPlayerPlayedMoves.length < 2) {
				nextMove = false;
			} else {
				for(var i=0,j=1; j<this._computerPlayerPlayedMoves.length; i++,j++) {
					for(var k=0; k<this._winningSequences.length; k++) {
						var match1 = this._winningSequences[k].indexOf(this._computerPlayerPlayedMoves[i]);
						var match2 = this._winningSequences[k].indexOf(this._computerPlayerPlayedMoves[j]);
						var thirdMatchIndex = 3 - (match1 + match2);
						var aggregateIndex = this._aggregatePlayedMoves.indexOf(this._winningSequences[k][thirdMatchIndex]);
						if( match1 !== -1 && match2 !== -1 &&  aggregateIndex === -1) {
							nextMove = this._winningSequences[k][thirdMatchIndex];
						}
					}
				}
			}

			return nextMove;
		}

		// passing in a boardIndex bypasses the AI
		makeMove(boardIndex?:number) {

			if(typeof boardIndex == "number") {
				super.makeMove(boardIndex); 
				this._computerPlayerPlayedMoves.push(boardIndex);
			} else {
				console.log(this.getLabel() + ' is using their wits...');
				var calculatedMove:number = this._calculate();
				super.makeMove(calculatedMove);
				this._computerPlayerPlayedMoves.push(calculatedMove);
				return calculatedMove;
			}
		}

		update(arg:any) {
			this._humanPlayerPlayedMoves.push(arg.madeMove);        	
	    }
	}
}