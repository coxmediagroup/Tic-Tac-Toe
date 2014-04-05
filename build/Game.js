/// <reference path="IObserver.ts" />
/// <reference path="PositionPrettyName.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Game = (function () {
        function Game() {
            this.players = [];
        }
        Game.prototype.update = function (arg) {
            console.log('Game has been notified and ' + arg.player + ' made move at position #' + arg.madeMove + ' aka ' + TicTacToe.PositionPrettyName[arg.madeMove]);
        };
        return Game;
    })();
    TicTacToe.Game = Game;
})(TicTacToe || (TicTacToe = {}));
