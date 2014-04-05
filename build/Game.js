/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Game = (function () {
        function Game() {
        }
        Game.prototype.update = function (arg) {
            console.log('Game has been notified and ' + arg.player + ' made move at position #' + arg.madeMove);
        };
        return Game;
    })();
    TicTacToe.Game = Game;
})(TicTacToe || (TicTacToe = {}));
