/// <reference path="IObserver.ts" /> 
module TicTacToe {
	// Primarily responsible for UI 
	export class Board implements IObserver {

		private _boardDiv;
		private _cells:any[] = [];

		constructor() {
			this._boardDiv = document.getElementById('board');
			this._boardDiv.setAttribute('style', 'width:600px;height:600px');
			this._boardDiv.style.display = 'block';
			this._boardDiv.style.width = '600px';
			this._boardDiv.style.height = '600px';
			this._boardDiv.style.border = '1px solid black';

			for(var i=0; i<9; i++) {
				var cell = document.createElement('canvas');
				cell.setAttribute('style', 'display:inline-block;float:left;margin:0;padding:0;width:200px;height:200px');
				cell.width = 200;
				cell.height = 200;
				var ctx = cell.getContext('2d');
				var alpha = i * .1;
				ctx.fillStyle = "rgba(0, 0, 200, " + alpha + ")";
  				ctx.fillRect (0, 0, 200, 200);
  				this._cells.push(cell);
  				this._boardDiv.appendChild(cell);
			}

		}

		update(arg:any) {
			   	console.log(arg);
	    }
	}
}