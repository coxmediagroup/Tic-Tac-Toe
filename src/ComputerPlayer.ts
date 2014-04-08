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
			[0,4,8],
			[2,4,6]
		];

		// returns the next calculated move
		private _calculate():number {
			var nextMove:number;
			this._computerPlayerPlayedMoves = super.getPlayedMoves();
			this._aggregatePlayedMoves = this._computerPlayerPlayedMoves.concat(this._humanPlayerPlayedMoves);
			 this._aggregatePlayedMoves.sort();
			 this._computerPlayerPlayedMoves.sort();
			 this._humanPlayerPlayedMoves.sort();
			 
			if(typeof this._checkTwoInARow(this._computerPlayerPlayedMoves) === 'number') {
				console.log('Computer Player is using _checkTwoInARow(computer) strategy.');
				nextMove = this._checkTwoInARow(this._computerPlayerPlayedMoves);
			} else if (typeof this._checkTwoInARow(this._humanPlayerPlayedMoves) === 'number') {
				console.log('Computer Player is using _checkTwoInARow(human) strategy.');
				nextMove = this._checkTwoInARow(this._humanPlayerPlayedMoves);
			} else if (typeof this._createFork() === 'number') {
				console.log('Computer Player is using _createFork() strategy.');
				nextMove = this._createFork();
			} else if (typeof this._blockFork() === 'number') {
				console.log('Computer Player is using _blockFork() strategy.');
				nextMove = this._blockFork();
			} else if (this._aggregatePlayedMoves.indexOf(4) === -1) {
				console.log('Computer Player is using playCenter strategy.');
				nextMove = 4;
			} else if (typeof this._playCorner() === 'number') {
				console.log('Computer Player is using _playCorner() strategy.');
				nextMove = this._playCorner();
			} else if (typeof this._playSide() === 'number') {
				console.log('Computer Player is using _playSide() strategy.');
				nextMove = this._playSide();
			}
			return nextMove;
		}

		// Returns the next optimal move if Computer Player can play a side
		private _playSide() {
			var nextMove:any;
			if(this._aggregatePlayedMoves.indexOf(1) === -1) {
				nextMove = 1;
			} else if (this._aggregatePlayedMoves.indexOf(3) === -1) {
				nextMove = 3;
			} else if (this._aggregatePlayedMoves.indexOf(5) === -1) {
				nextMove = 5;
			} else if (this._aggregatePlayedMoves.indexOf(7) === -1) {
				nextMove = 7;
			} else {
				nextMove = false;
			}

			return nextMove;
		}

		// Returns the next optimal move if Computer Player can play a corner
		// Otherwise, returns false.
		private _playCorner() {
			var nextMove:any;
			if(this._aggregatePlayedMoves.indexOf(0) === -1) {
				nextMove = 0;
			} else if (this._aggregatePlayedMoves.indexOf(2) === -1) {
				nextMove = 2;
			} else if (this._aggregatePlayedMoves.indexOf(6) === -1) {
				nextMove = 6;
			} else if (this._aggregatePlayedMoves.indexOf(8) === -1) {
				nextMove = 8;
			} else {
				nextMove = false;
			}

			return nextMove;
		}

		// Returns the next optimal move if opponent can fork on their next turn.
		// Otherwise, returns false.
		private _blockFork() {
			var nextMove:any;
			var matchedWinningSequences:any[] = [];

			// find all winning sequences that contain at least one played move
			for(var i=0; i<this._winningSequences.length; i++) {
				var sequence = this._winningSequences[i];
				for(var j=0; j<3; j++) {
					if(this._humanPlayerPlayedMoves.indexOf(sequence[j]) !== -1) {
						matchedWinningSequences.push(sequence);
						break;
					}
				}
			}

			// Find the first pair of matched winning sequences that shares an unplayed position and return that position.
			// Otherwise, return false.
			for(var i = 0; i<matchedWinningSequences.length; i++) {
				for (var j=0; j<matchedWinningSequences.length; j++) {
					if(j !== i) {
						var possibleNextMoves = this._intersect(matchedWinningSequences[i], matchedWinningSequences[j]);
						for(var k=0; k<possibleNextMoves.length; k++) {
							if(this._aggregatePlayedMoves.indexOf(possibleNextMoves[k]) === -1) {
								var nextPossibleMove = possibleNextMoves[k];
								nextMove = parseInt(nextPossibleMove, 10);
								return nextMove;
							}
						}
					}
				}
			}

			return nextMove = false;
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
					if(j !== i) {
						var possibleNextMoves = this._intersect(matchedWinningSequences[i], matchedWinningSequences[j]);
						for(var k=0; k<possibleNextMoves.length; k++) {
							if(this._aggregatePlayedMoves.indexOf(possibleNextMoves[k]) === -1) {
								var nextPossibleMove = possibleNextMoves[k];
								nextMove = parseInt(nextPossibleMove, 10);

								if(this._aggregatePlayedMoves.indexOf(nextMove) === -1) {
									return nextMove;
								} else {
									nextMove = false;
								}
								
							}
						}
					}
				}
			}

			return nextMove = false;
		}

		private _intersect(a, b) {
		  var ai=0, bi=0;
		  var result = new Array();

		  while( ai < a.length && bi < b.length )
		  {
		     if      (a[ai] < b[bi] ){ ai++; }
		     else if (a[ai] > b[bi] ){ bi++; }
		     else /* they're equal */
		     {
		       result.push(a[ai]);
		       ai++;
		       bi++;
		     }
		  }

		  return result;
		}

		// Returns the next optimal move if argument supplied for @playerMoves has played at least 2/3 moves in any of the winning sequences.
		// Otherwise, returns false.
		private _checkTwoInARow(playerMoves):any {
			var nextMove:any;

			if(playerMoves.length < 2) {
				nextMove = false;
			} else {
				var matchedWinningSequences = [];
				for(var i = 0; i<playerMoves.length; i++) {
					for(var j = 0; j<this._winningSequences.length; j++) {
						if(this._winningSequences[j].indexOf(playerMoves[i]) !== -1) {
							matchedWinningSequences.push(this._winningSequences[j]);
						}
					}
				}

				for(var i=0; i<matchedWinningSequences.length; i++) {
				
					if(this._intersect(matchedWinningSequences[i], playerMoves).length === 2) {
						
						
						var nextMoveArray = this._diff(matchedWinningSequences[i], playerMoves);
						

						for (var j = 0; j<nextMoveArray.length; j++) {

							if(this._aggregatePlayedMoves.indexOf(nextMoveArray[j]) === -1) {
								
								nextMove = parseInt(nextMoveArray[j],10);

								if(this._aggregatePlayedMoves.indexOf(nextMove) === -1) {
									return nextMove;
								} else {
									nextMove = false;
								}
							}
						}
						

					}
				}

			}
			
			
			return nextMove;
		}

		private _diff(a1, a2) {
			var a=[], diff=[];
		  for(var i=0;i<a1.length;i++)
		    a[a1[i]]=true;
		  for(var i=0;i<a2.length;i++)
		    if(a[a2[i]]) delete a[a2[i]];
		    else a[a2[i]]=true;
		  for(var k in a)
		    diff.push(k);
		  return diff;
		}

		private _reset() {
			console.log('Computer Player is resetting...');
			console.log('');
			this._humanPlayerPlayedMoves = [];
	    	this._computerPlayerPlayedMoves = [];
	    	this._aggregatePlayedMoves = [];
	    	super.reset();
		}

		// passing in a boardIndex bypasses the AI
		makeMove(boardIndex?:number) {

			if(typeof boardIndex == "number") {
				super.makeMove(boardIndex); 
			} else {
				console.log(this.getLabel() + ' is using their wits...');
				var calculatedMove:number = this._calculate();
				super.makeMove(calculatedMove);
				return calculatedMove;
			}
		}

		update(arg:any) {
			
			if(arg.draw === 'true' || typeof arg.winner === 'string') { 
				this._reset();
			} else if(arg.player === 'Human Player' && typeof arg.madeMove === 'number') { 
				this._humanPlayerPlayedMoves.push(arg.madeMove); 
			} 
			
	    }

	    reset() {
	    	this._reset();
	    }
	}
}