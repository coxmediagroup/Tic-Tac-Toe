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
				cell.setAttribute('class', 'cell');
				cell.setAttribute('played', 'false');
				cell.setAttribute('cellIndex', i.toString());
				cell.width = 200;
				cell.height = 200;
				var ctx = cell.getContext('2d');
				
				// cell border
				ctx.strokeStyle = "rgb(0, 0, 0)";
				ctx.fillStyle = "rgb(0, 0, 0)";
  				ctx.strokeRect (0, 0, 200, 200);


	     //        ctx.lineWidth = 20;

  				// // Stroked line vertical
			   //  ctx.beginPath();
			   //  ctx.moveTo(100,0);
			   //  ctx.lineTo(100,200);
			   //  ctx.closePath();
			   //  ctx.stroke();

			   //  // Stroked line horizontal
			   //  ctx.beginPath();
			   //  ctx.moveTo(0,100);
			   //  ctx.lineTo(200,100);
			   //  ctx.closePath();
			   //  ctx.stroke();

  				this._cells.push(cell);
  				this._boardDiv.appendChild(cell);
			}


			// var cellClassName = document.getElementsByClassName("cell");

			// var that = this;

		 //   var cellClickHandler = function() {
		 //       var played = this.getAttribute("played");
		 //       if(played === 'true') {
		 //       	alert('Position has already been played.');
		 //       } else {
		 //       	that._makeMove('Human Player', this.getAttribute("cellIndex"));
		 //       }
		 //    };

		 //    for(var i=0;i<cellClassName.length;i++){
		 //      cellClassName[i].addEventListener('click', cellClickHandler, false);
		 //    }


		}

		private _makeMove(player, cell) {

			var ctx = this._cells[cell].getContext('2d');	
			var color:string;
			var text:string;
			var nextPlayer:string;
			if(player === 'Human Player') {
				color = 'red';
				text = 'X';
				nextPlayer = 'Computer Player';
			} else {
				color = 'black';
				text = 'O';
				nextPlayer = 'Human Player';
			}		 
		    ctx.fillStyle = color;
            ctx.font = "200pt Helvetica";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(text, this._cells[cell].width / 2 , this._cells[cell].height / 2);
            document.getElementById("nextPlayer").innerHTML = nextPlayer;
            this._cells[cell].setAttribute('played', 'true');
		}

		private _reset(arg) {
			document.getElementById("humanScore").innerHTML = arg.humanScore;
			document.getElementById("computerScore").innerHTML = arg.computerScore;
			document.getElementById("nextPlayer").innerHTML = 'Human Player';

			for(var i = 0; i<this._cells.length; i++) {
				var ctx = this._cells[i].getContext('2d');	
				// cell border
				ctx.strokeStyle = "rgb(0, 0, 0)";
				ctx.fillStyle = "rgb(255, 255, 255)";
				ctx.fillRect(0,0,200,200);
  				ctx.strokeRect (0, 0, 200, 200);
  				this._cells[i].setAttribute('played', 'false');

			}
		}

		update(arg:any) {
			   	

			   	if(arg.player && typeof arg.move === 'number') {
			   		this._makeMove(arg.player, arg.move);
			   	} else if (typeof arg.humanScore === 'number' && typeof arg.computerScore === 'number') {
			   		alert('Winner: ' + arg.winner);
			   		this._reset(arg);
			   	} 
	    }
	}
}