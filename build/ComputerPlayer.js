var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
/// <reference path="Player.ts" />
/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    var ComputerPlayer = (function (_super) {
        __extends(ComputerPlayer, _super);
        function ComputerPlayer() {
            _super.call(this, "Computer Player");
            this._computerPlayerPlayedMoves = [];
            this._humanPlayerPlayedMoves = [];
            this._aggregatePlayedMoves = [];
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
        // returns the next calculated move
        ComputerPlayer.prototype._calculate = function () {
            var nextMove;
            this._aggregatePlayedMoves = this._computerPlayerPlayedMoves.concat(this._humanPlayerPlayedMoves);
            if (typeof this._checkTwoInARow() === 'number') {
                nextMove = this._checkTwoInARow();
            }
            return nextMove;
        };

        // returns next move or false
        ComputerPlayer.prototype._checkTwoInARow = function () {
            var nextMove;

            if (this._computerPlayerPlayedMoves.length < 2) {
                nextMove = false;
            } else {
                for (var i = 0, j = 1; j < this._computerPlayerPlayedMoves.length; i++, j++) {
                    for (var k = 0; k < this._winningSequences.length; k++) {
                        var match1 = this._winningSequences[k].indexOf(this._computerPlayerPlayedMoves[i]);
                        var match2 = this._winningSequences[k].indexOf(this._computerPlayerPlayedMoves[j]);
                        var thirdMatchIndex = 3 - (match1 + match2);
                        var aggregateIndex = this._aggregatePlayedMoves.indexOf(this._winningSequences[k][thirdMatchIndex]);
                        if (match1 !== -1 && match2 !== -1 && aggregateIndex === -1) {
                            nextMove = this._winningSequences[k][thirdMatchIndex];
                        }
                    }
                }
            }

            return nextMove;
        };

        // passing in a boardIndex bypasses the AI
        ComputerPlayer.prototype.makeMove = function (boardIndex) {
            if (typeof boardIndex == "number") {
                _super.prototype.makeMove.call(this, boardIndex);
                this._computerPlayerPlayedMoves.push(boardIndex);
            } else {
                console.log(this.getLabel() + ' is using their wits...');
                var calculatedMove = this._calculate();
                _super.prototype.makeMove.call(this, calculatedMove);
                this._computerPlayerPlayedMoves.push(calculatedMove);
                return calculatedMove;
            }
        };

        ComputerPlayer.prototype.update = function (arg) {
            this._humanPlayerPlayedMoves.push(arg.madeMove);
        };
        return ComputerPlayer;
    })(TicTacToe.Player);
    TicTacToe.ComputerPlayer = ComputerPlayer;
})(TicTacToe || (TicTacToe = {}));
