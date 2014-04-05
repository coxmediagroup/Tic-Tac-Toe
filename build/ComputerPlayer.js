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
            if (typeof this._checkTwoInARow(this._computerPlayerPlayedMoves) === 'number') {
                nextMove = this._checkTwoInARow(this._computerPlayerPlayedMoves);
            } else if (typeof this._checkTwoInARow(this._humanPlayerPlayedMoves) === 'number') {
                nextMove = this._checkTwoInARow(this._humanPlayerPlayedMoves);
            } else if (typeof this._createFork() === 'number') {
                nextMove = this._createFork();
            }
            return nextMove;
        };

        // Returns the next optimal move if a forking opportunity exists.
        // Otherwise, returns false.
        ComputerPlayer.prototype._createFork = function () {
            var nextMove;
            var matchedWinningSequences = [];

            for (var i = 0; i < this._winningSequences.length; i++) {
                var sequence = this._winningSequences[i];
                for (var j = 0; j < 3; j++) {
                    if (this._computerPlayerPlayedMoves.indexOf(sequence[j]) !== -1) {
                        matchedWinningSequences.push(sequence);
                        break;
                    }
                }
            }

            for (var i = 0; i < matchedWinningSequences.length; i++) {
                for (var j = 0; j < matchedWinningSequences.length; j++) {
                    if (j !== i) {
                        var possibleNextMoves = this._intersect(matchedWinningSequences[i], matchedWinningSequences[j]);
                        for (var k = 0; k < possibleNextMoves.length; k++) {
                            if (this._aggregatePlayedMoves.indexOf(possibleNextMoves[k]) === -1) {
                                return nextMove = possibleNextMoves[k];
                            }
                        }
                    }
                }
            }

            return nextMove = false;
        };

        ComputerPlayer.prototype._intersect = function (a, b) {
            var ai = 0, bi = 0;
            var result = new Array();

            while (ai < a.length && bi < b.length) {
                if (a[ai] < b[bi]) {
                    ai++;
                } else if (a[ai] > b[bi]) {
                    bi++;
                } else {
                    result.push(a[ai]);
                    ai++;
                    bi++;
                }
            }

            return result;
        };

        // Returns the next optimal move if argument supplied for @playerMoves has played at least 2/3 moves in any of the winning sequences.
        // Otherwise, returns false.
        ComputerPlayer.prototype._checkTwoInARow = function (playerMoves) {
            var nextMove;

            if (playerMoves.length < 2) {
                nextMove = false;
            } else {
                for (var i = 0, j = 1; j < playerMoves.length; i++, j++) {
                    for (var k = 0; k < this._winningSequences.length; k++) {
                        var match1 = this._winningSequences[k].indexOf(playerMoves[i]);
                        var match2 = this._winningSequences[k].indexOf(playerMoves[j]);
                        var thirdMatchIndex = 3 - (match1 + match2);
                        var aggregateIndex = this._aggregatePlayedMoves.indexOf(this._winningSequences[k][thirdMatchIndex]);
                        if (match1 !== -1 && match2 !== -1 && aggregateIndex === -1) {
                            return nextMove = this._winningSequences[k][thirdMatchIndex];
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
