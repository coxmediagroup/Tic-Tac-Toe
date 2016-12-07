var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
/// <reference path="Observable.ts" />
/// <reference path="IObserver.ts" />
/// <reference path="PositionPrettyName.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Game = (function (_super) {
        __extends(Game, _super);
        function Game() {
            _super.call(this);
            this._computerPlayerPlayedMoves = [];
            this._humanPlayerPlayedMoves = [];
            this._aggregatePlayedMoves = [];
            this._nextPlayer = 'Human Player';
            this._winner = false;
            this._humanScore = 0;
            this._computerScore = 0;
            this._winningSequences = [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 4, 8],
                [2, 4, 6]
            ];
        }
        Game.prototype._checkForWinner = function () {
            // check if human player has played at least three moves
            if (this._humanPlayerPlayedMoves.length >= 3) {
                for (var i = 0; i < this._winningSequences.length; i++) {
                    var match1 = this._humanPlayerPlayedMoves.indexOf(this._winningSequences[i][0]);
                    var match2 = this._humanPlayerPlayedMoves.indexOf(this._winningSequences[i][1]);
                    var match3 = this._humanPlayerPlayedMoves.indexOf(this._winningSequences[i][2]);
                    if (match1 !== -1 && match2 !== -1 && match3 !== -1) {
                        console.log('Winner is Human Player.');
                        this._humanScore++;
                        this._winner = 'Human Player';
                        this._reset('Human Player'); // winner goes first
                        return;
                    }
                }
            }

            // check if computer player has played at least three moves
            if (this._computerPlayerPlayedMoves.length >= 3) {
                for (var i = 0; i < this._winningSequences.length; i++) {
                    var match1 = this._computerPlayerPlayedMoves.indexOf(this._winningSequences[i][0]);
                    var match2 = this._computerPlayerPlayedMoves.indexOf(this._winningSequences[i][1]);
                    var match3 = this._computerPlayerPlayedMoves.indexOf(this._winningSequences[i][2]);
                    if (match1 !== -1 && match2 !== -1 && match3 !== -1) {
                        console.log('Winner is Computer Player.');
                        this._computerScore++;
                        this._winner = 'Computer Player';
                        this._reset('Computer Player'); // winner goes first
                        return;
                    }
                }
            }

            // check if draw
            if (this._aggregatePlayedMoves.length >= 9) {
                console.log('Draw.');
                this._reset('Draw');
            }

            return this._winner = false;
        };

        Game.prototype._reset = function (nextPlayer) {
            console.log('Game over.');
            console.log('Human Score: ' + this._humanScore);
            console.log('Computer Score: ' + this._computerScore);
            console.log('');

            if (nextPlayer === 'Draw') {
                this.notifyObservers({ draw: 'true' });
            } else {
                this.notifyObservers({ humanScore: this._humanScore, computerScore: this._computerScore, winner: nextPlayer });
                this._nextPlayer = nextPlayer;
            }

            this._computerPlayerPlayedMoves = [];
            this._humanPlayerPlayedMoves = [];
            this._aggregatePlayedMoves = [];
        };

        Game.prototype.getWinner = function () {
            return this._winner;
        };

        Game.prototype.update = function (arg) {
            console.log('Game has been notified and ' + arg.player + ' made move at position #' + arg.madeMove + ' aka ' + TicTacToe.PositionPrettyName[arg.madeMove]);

            if (arg.player === 'Computer Player') {
                this._computerPlayerPlayedMoves.push(arg.madeMove);
                this._nextPlayer = 'Human Player';
            } else {
                this._humanPlayerPlayedMoves.push(arg.madeMove);
                this._nextPlayer = 'Computer Player';
            }
            this._aggregatePlayedMoves.push(arg.madeMove);
            this.notifyObservers({ player: arg.player, move: arg.madeMove });

            this._checkForWinner();
        };
        return Game;
    })(TicTacToe.Observable);
    TicTacToe.Game = Game;
})(TicTacToe || (TicTacToe = {}));
