/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    // Primarily responsible for UI
    var Board = (function () {
        function Board() {
            this._cells = [];
            this._boardDiv = document.getElementById('board');
            this._boardDiv.setAttribute('style', 'width:600px;height:600px');
            this._boardDiv.style.display = 'block';
            this._boardDiv.style.width = '600px';
            this._boardDiv.style.height = '600px';
            this._boardDiv.style.border = '1px solid black';

            for (var i = 0; i < 9; i++) {
                var cell = document.createElement('canvas');
                cell.setAttribute('style', 'display:inline-block;float:left;margin:0;padding:0;width:200px;height:200px');
                cell.width = 200;
                cell.height = 200;
                var ctx = cell.getContext('2d');

                // cell border
                ctx.strokeStyle = "rgb(0, 0, 0)";
                ctx.fillStyle = "rgb(0, 0, 0)";
                ctx.strokeRect(0, 0, 200, 200);

                //X
                ctx.fillStyle = "red";
                ctx.font = "200pt Helvetica";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText("X", cell.width / 2, cell.height / 2);

                //O
                ctx.fillStyle = "black";
                ctx.font = "200pt Helvetica";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText("O", cell.width / 2, cell.height / 2);

                ctx.lineWidth = 20;

                // Stroked line vertical
                ctx.beginPath();
                ctx.moveTo(100, 0);
                ctx.lineTo(100, 200);
                ctx.closePath();
                ctx.stroke();

                // Stroked line horizontal
                ctx.beginPath();
                ctx.moveTo(0, 100);
                ctx.lineTo(200, 100);
                ctx.closePath();
                ctx.stroke();

                this._cells.push(cell);
                this._boardDiv.appendChild(cell);
            }
        }
        Board.prototype.update = function (arg) {
            console.log(arg);
        };
        return Board;
    })();
    TicTacToe.Board = Board;
})(TicTacToe || (TicTacToe = {}));
