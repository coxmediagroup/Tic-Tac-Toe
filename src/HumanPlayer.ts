/// <reference path="Player.ts" />
module TicTacToe {
	export class HumanPlayer extends Player { 
		constructor() { super("Human Player"); }

		makeMove(boardIndex:number) {
			super.makeMove(boardIndex);
		}
	}     
}  