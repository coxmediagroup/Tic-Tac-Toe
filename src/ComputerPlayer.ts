/// <reference path="Player.ts" />
/// <reference path="IObserver.ts" /> 
module TicTacToe { 
	export class ComputerPlayer extends Player implements IObserver {
		constructor() { super("Computer Player"); }

		private _computerPlayerPlayedMoves:number[] = [];
		private _humanPlayerPlayedMoves:number[] = [];

		private _calculate() {
			return 999;
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