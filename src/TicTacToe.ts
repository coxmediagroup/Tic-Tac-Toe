module TicTacToe {
	export class Player {
		private _score: number = 0;

		constructor(private _label: string) { }

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