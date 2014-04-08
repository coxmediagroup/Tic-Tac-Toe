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
                [0, 4, 8],
                [2, 4, 6]
            ];
        }
        // returns the next calculated move
        ComputerPlayer.prototype._calculate = function () {
            var nextMove;
            this._aggregatePlayedMoves = this._computerPlayerPlayedMoves.concat(this._humanPlayerPlayedMoves);
            this._aggregatePlayedMoves.sort();
            this._computerPlayerPlayedMoves.sort();
            this._humanPlayerPlayedMoves.sort();

            if (typeof this._checkTwoInARow(this._computerPlayerPlayedMoves) === 'number') {
                console.log('Computer Player is using _checkTwoInARow(computer) strategy.');
                nextMove = this._checkTwoInARow(this._computerPlayerPlayedMoves);
            } else if (typeof this._checkTwoInARow(this._humanPlayerPlayedMoves) === 'number') {
                console.log('Computer Player is using _checkTwoInARow(human) strategy.');
                nextMove = this._checkTwoInARow(this._humanPlayerPlayedMoves);
            } else if (typeof this._createFork() === 'number') {
                console.log('Computer Player is using _createFork() strategy.');
                nextMove = this._createFork();
            } else if (typeof this._blockFork() === 'number') {
                console.log('Computer Player is using _blockFork() strategy.');
                nextMove = this._blockFork();
            } else if (this._aggregatePlayedMoves.indexOf(4) === -1) {
                console.log('Computer Player is using playCenter strategy.');
                nextMove = 4;
            } else if (typeof this._playCorner() === 'number') {
                console.log('Computer Player is using _playCorner() strategy.');
                nextMove = this._playCorner();
            } else if (typeof this._playSide() === 'number') {
                console.log('Computer Player is using _playSide() strategy.');
                nextMove = this._playSide();
            }
            return nextMove;
        };

        // Returns the next optimal move if Computer Player can play a side
        ComputerPlayer.prototype._playSide = function () {
            var nextMove;
            if (this._aggregatePlayedMoves.indexOf(1) === -1) {
                nextMove = 1;
            } else if (this._aggregatePlayedMoves.indexOf(3) === -1) {
                nextMove = 3;
            } else if (this._aggregatePlayedMoves.indexOf(5) === -1) {
                nextMove = 5;
            } else if (this._aggregatePlayedMoves.indexOf(7) === -1) {
                nextMove = 7;
            } else {
                nextMove = false;
            }

            return nextMove;
        };

        // Returns the next optimal move if Computer Player can play a corner
        // Otherwise, returns false.
        ComputerPlayer.prototype._playCorner = function () {
            var nextMove;
            if (this._aggregatePlayedMoves.indexOf(0) === -1) {
                nextMove = 0;
            } else if (this._aggregatePlayedMoves.indexOf(2) === -1) {
                nextMove = 2;
            } else if (this._aggregatePlayedMoves.indexOf(6) === -1) {
                nextMove = 6;
            } else if (this._aggregatePlayedMoves.indexOf(8) === -1) {
                nextMove = 8;
            } else {
                nextMove = false;
            }

            return nextMove;
        };

        // Returns the next optimal move if opponent can fork on their next turn.
        // Otherwise, returns false.
        ComputerPlayer.prototype._blockFork = function () {
            var nextMove;
            var matchedWinningSequences = [];

            for (var i = 0; i < this._winningSequences.length; i++) {
                var sequence = this._winningSequences[i];
                for (var j = 0; j < 3; j++) {
                    if (this._humanPlayerPlayedMoves.indexOf(sequence[j]) !== -1) {
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
                                var nextPossibleMove = possibleNextMoves[k];
                                nextMove = parseInt(nextPossibleMove, 10);
                                return nextMove;
                            }
                        }
                    }
                }
            }

            return nextMove = false;
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
                                var nextPossibleMove = possibleNextMoves[k];
                                nextMove = parseInt(nextPossibleMove, 10);

                                if (this._aggregatePlayedMoves.indexOf(nextMove) === -1) {
                                    return nextMove;
                                } else {
                                    nextMove = false;
                                }
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
                var matchedWinningSequences = [];
                for (var i = 0; i < playerMoves.length; i++) {
                    for (var j = 0; j < this._winningSequences.length; j++) {
                        if (this._winningSequences[j].indexOf(playerMoves[i]) !== -1) {
                            matchedWinningSequences.push(this._winningSequences[j]);
                        }
                    }
                }

                for (var i = 0; i < matchedWinningSequences.length; i++) {
                    if (this._intersect(matchedWinningSequences[i], playerMoves).length === 2) {
                        var nextMoveArray = this._diff(matchedWinningSequences[i], playerMoves);

                        for (var j = 0; j < nextMoveArray.length; j++) {
                            if (this._aggregatePlayedMoves.indexOf(nextMoveArray[j]) === -1) {
                                nextMove = parseInt(nextMoveArray[j], 10);

                                if (this._aggregatePlayedMoves.indexOf(nextMove) === -1) {
                                    return nextMove;
                                } else {
                                    nextMove = false;
                                }
                            }
                        }
                    }
                }
            }

            return nextMove;
        };

        ComputerPlayer.prototype._diff = function (a1, a2) {
            var a = [], diff = [];
            for (var i = 0; i < a1.length; i++)
                a[a1[i]] = true;
            for (var i = 0; i < a2.length; i++)
                if (a[a2[i]])
                    delete a[a2[i]];
                else
                    a[a2[i]] = true;
            for (var k in a)
                diff.push(k);
            return diff;
        };

        ComputerPlayer.prototype._reset = function () {
            this._humanPlayerPlayedMoves = [];
            this._computerPlayerPlayedMoves = [];
            this._aggregatePlayedMoves = [];
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
            console.log(arg);
            this._humanPlayerPlayedMoves.push(arg.madeMove);
        };

        ComputerPlayer.prototype.reset = function () {
            this._reset();
        };
        return ComputerPlayer;
    })(TicTacToe.Player);
    TicTacToe.ComputerPlayer = ComputerPlayer;
})(TicTacToe || (TicTacToe = {}));
