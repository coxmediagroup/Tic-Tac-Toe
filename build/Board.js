/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Board = (function () {
        function Board() {
            this._boardDiv = document.getElementById('board');
            this._boardDiv.setAttribute('style', 'width:600px;height:600px');
            this._boardDiv.style.display = 'block';
            this._boardDiv.style.width = '600px';
            this._boardDiv.style.height = '600px';
            this._boardDiv.style.border = '1px solid black';
        }
        Board.prototype.update = function (arg) {
            console.log(arg);
        };
        return Board;
    })();
    TicTacToe.Board = Board;
})(TicTacToe || (TicTacToe = {}));
