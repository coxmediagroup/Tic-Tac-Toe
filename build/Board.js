/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Board = (function () {
        function Board() {
        }
        Board.prototype.update = function (arg) {
        };
        return Board;
    })();
    TicTacToe.Board = Board;
})(TicTacToe || (TicTacToe = {}));
