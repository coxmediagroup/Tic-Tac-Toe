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
			if(typeof this._checkTwoInARow(this._computerPlayerPlayedMoves) === 'number') {
				nextMove = this._checkTwoInARow(this._computerPlayerPlayedMoves);
			} else if (typeof this._checkTwoInARow(this._humanPlayerPlayedMoves) === 'number') {
				nextMove = this._checkTwoInARow(this._humanPlayerPlayedMoves);
			} else if (typeof this._createFork() === 'number') {
				nextMove = this._createFork();
			}
			return nextMove;
		}

		// Returns the next optimal move if a forking opportunity exists.
		// Otherwise, returns false.
		private _createFork() {
			var nextMove:any;
			var matchedWinningSequences:any[] = [];

			// find all winning sequences that contain at least one played move
			for(var i=0; i<this._winningSequences.length; i++) {
				var sequence = this._winningSequences[i];
				for(var j=0; j<3; j++) {
					if(this._computerPlayerPlayedMoves.indexOf(sequence[j]) !== -1) {
						matchedWinningSequences.push(sequence);
						break;
					}
				}
			}

			// Find the first pair of matched winning sequences that shares an unplayed position and return that position.
			// Otherwise, return false.
			for(var i = 0; i<matchedWinningSequences.length; i++) {
				for (var j=0; j<matchedWinningSequences.length; j++) {
					var possibleNextMoveIndex = matchedWinningSequences[i].indexOf(matchedWinningSequences[j]);
					if(j !== i && possibleNextMoveIndex !== -1) {
						var possibleNextMove = matchedWinningSequences[possibleNextMoveIndex];
						if(this._aggregatePlayedMoves.indexOf(possibleNextMove) === -1) {
							return nextMove = possibleNextMove;
						}
					}
				}
			}

			return nextMove = false;
		}

		// Returns the next optimal move if argument supplied for @playerMoves has played at least 2/3 moves in any of the winning sequences.
		// Otherwise, returns false.
		private _checkTwoInARow(playerMoves):any {
			var nextMove:any;

			if(playerMoves.length < 2) {
				nextMove = false;
			} else {
				for(var i=0,j=1; j<playerMoves.length; i++,j++) {
					for(var k=0; k<this._winningSequences.length; k++) {
						var match1 = this._winningSequences[k].indexOf(playerMoves[i]);
						var match2 = this._winningSequences[k].indexOf(playerMoves[j]);
						var thirdMatchIndex = 3 - (match1 + match2);
						var aggregateIndex = this._aggregatePlayedMoves.indexOf(this._winningSequences[k][thirdMatchIndex]);
						if( match1 !== -1 && match2 !== -1 &&  aggregateIndex === -1) {
							return nextMove = this._winningSequences[k][thirdMatchIndex];
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