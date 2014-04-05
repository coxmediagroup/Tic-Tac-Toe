/// <reference path="Observable.ts" /> 
module TicTacToe {

	export class Player extends Observable {
		private _score: number = 0;
		private _playedMoves: number[] = [];

		constructor(private _label: string) { 
			super();
		}

		makeMove(boardIndex:number): void {
			this._playedMoves.push(boardIndex); 
			this.notifyObservers({player:this._label,madeMove:boardIndex});
		}

		// TODO: Set the compiler to output ECMAScript 5 and convert to a proper getter.
		getLabel(): string {
        	return this._label;
    	} 
		
		getScore(): number {
			return this._score;
		}

		setScore(score: number) {
			this._score = score;

		} 

	} 
}