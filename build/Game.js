/// <reference path="IObserver.ts" />
/// <reference path="PositionPrettyName.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Game = (function () {
        function Game() {
            this._computerPlayerPlayedMoves = [];
            this._humanPlayerPlayedMoves = [];
            this._winner = false;
            this._winningSequences = [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 5, 8],
                [2, 5, 6]
            ];
        }
        Game.prototype._checkForWinner = function () {
        };

        Game.prototype.getWinner = function () {
            return this._winner;
        };

        Game.prototype.update = function (arg) {
            console.log('Game has been notified and ' + arg.player + ' made move at position #' + arg.madeMove + ' aka ' + TicTacToe.PositionPrettyName[arg.madeMove]);

            if (arg.player === 'Computer Player') {
                this._computerPlayerPlayedMoves.push(arg.madeMove);
            } else {
                this._humanPlayerPlayedMoves.push(arg.madeMove);
            }

            this._checkForWinner();
        };
        return Game;
    })();
    TicTacToe.Game = Game;
})(TicTacToe || (TicTacToe = {}));
