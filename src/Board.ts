/// <reference path="IObserver.ts" /> 
module TicTacToe {
	export class Board implements IObserver {

		private _boardDiv;

		constructor() {
			this._boardDiv = document.getElementById('board');
			this._boardDiv.setAttribute('style', 'width:600px;height:600px');
			this._boardDiv.style.display = 'block';
			this._boardDiv.style.width = '600px';
			this._boardDiv.style.height = '600px';
			this._boardDiv.style.border = '1px solid black';
		}

		update(arg:any) {
			   	console.log(arg);
	    }
	}
}