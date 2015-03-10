var express = require('express');
var router = express.Router();
var appLogger = require('../logger/logger');
var logger = appLogger.LOG;

/*
 * PLACEHOLDER FOR DELETION
 * 
 * REALLY SHOULD SOLVE USING MINMATRIX ALGORITHM INSTEAD
 */
var firstMove = false;
var BoardOperations = {

    /**
     * 
     */
    arrayToJSON : function(array) {
        console.log(JSON.stringify(array));
        return JSON.stringify(array);
    },

    /**
     * 
     */
    jsonToArray : function(json) {
        console.log("JSON TO ARRAY");
        console.log(JSON.parse(json));
        return JSON.parse(json);

    },

    /**
     * 
     */
    doit : function() {
        logger.debug("Done!");
    },

    /**
     * 
     */
    checkwin : function(board) {

        logger.debug("Checking Board for Winner! ");

        logger.debug("Board: " + JSON.stringify(board));
        var b = this.jsonToArray(board);
        var winner = this.isWinner(b);
        logger.debug("isWinner? " + winner);
        return winner;

    },

    /**
     * TODO:
     */
    block : function(gameboard) {
        var newboard = gameboard;

        var blocked = false;

        // not checking for a winning move for 'O' here is causing a bug .. AI
        // will block instead of making winning move
        // winMove();
        // PLAYER can win if forces side then corner moves (1,1), (1,2), (2.,0),
        // (2,1)...

        // check for 2 in a row horizontal and replace
        for (var i = 0; i < newboard.length; i++) {

            // horizontal pair
            if (newboard[i][0] == 'X' && newboard[i][1] == 'X') {
                if (newboard[i][2] == null) {
                    newboard[i][2] = 'O';
                    blocked = true;
                }
            }

            // horizontal pair
            if (newboard[i][1] == 'X' && newboard[i][2] == 'X') {
                if (newboard[i][0] == null) {
                    newboard[i][0] = 'O';
                    blocked = true;
                }
            }
        }

        if (blocked) {
            return newboard;
        }

        // check for vertical cases
        for (var i = 0; i < newboard.length; i++) {

            // vertical pair
            if (newboard[0][i] == 'X' && newboard[1][i] == 'X') {
                if (newboard[2][i] == null) {
                    newboard[2][i] = 'O';
                    blocked = true;
                }
            }

            // vertical pair
            if (newboard[1][i] == 'X' && newboard[2][i] == 'X') {
                if (newboard[0][i] == null) {
                    newboard[0][i] = 'O';
                    blocked = true;
                }
            }
        }

        if (blocked) {
            return newboard;
        }

        // this is nasty and can be cleaned by using a recursive predition
        // matrix algorithm
        if (newboard[0][0] == 'X' && newboard[0][2] == 'X') {
            // blocked at 0,1
            if (newboard[0][1] == null) {
                newboard[0][1] = 'O';
                blocked = true;
            }
        } else if (newboard[0][0] == 'X' && newboard[2][0] == 'X') {
            // blocked at 1, 0
            if (newboard[1][0] == null) {
                newboard[1][0] = 'O';
                blocked = true;
            }
        } else if (newboard[0][2] == 'X' && newboard[2][2] == 'X') {
            // blocked at 1,2
            if (newboard[1][2] == null) {
                newboard[1][2] = 'O';
                blocked = true;
            }
        } else if (newboard[2][0] == 'X' && newboard[2][2] == 'X') {
            // blocked at 2,1
            if (newboard[2][1] == null) {
                newboard[2][1] = 'O';
                blocked = true;
            }
        } else if (newboard[0][0] == 'X' && newboard[1][1] == 'X') {
            // blocked at 2,1
            if (newboard[2][2] == null) {
                newboard[2][2] = 'O';
                blocked = true;
            }
        } else if (newboard[0][2] == 'X' && newboard[1][1] == 'X') {
            // blocked at 2,1
            if (newboard[2][0] == null) {
                newboard[2][0] = 'O';
                blocked = true;
            }
        } else if (newboard[2][2] == 'X' && newboard[1][1] == 'X') {
            // blocked at 2,1
            if (newboard[0][0] == null) {
                newboard[0][0] = 'O';
                blocked = true;
            }
        } else if (newboard[2][0] == 'X' && newboard[1][1] == 'X') {
            // blocked at 2,1
            if (newboard[0][2] == null) {
                newboard[0][2] = 'O';
                blocked = true;
            }
        }

        if (blocked) {
            return newboard;
        }

        //
        for (var i = 0; i < newboard.length; i++) {
            var totalOccurs = newboard[i].filter(function(value) {
                return value === 'X';
            }).length;

            if (totalOccurs == 1) {

                for (var j = 0; j < newboard.length; j++) {
                    if (newboard[i][j] == null) {
                        newboard[i][j] = 'O';
                        return newboard;
                    }

                }
            }
        }

        logger.debug("NO BLOCKS");
        return newboard;

    },
    initialMove : function(board) {
        var b = board;
        if (b[1][1] == null) {
            b[1][1] = 'O';
        } else {

            if (b[0][0] == null) {
                b[0][0] = 'O';
            } else if (b[0][2] == null) {
                b[0][2] = 'O';
            } else if (b[2][0] == null) {
                b[2][0] = 'O';
            } else if (b[2][2] == null) {
                b[2][2] = 'O';
            }

        }
        return b;
    },
    /**
     * 
     */
    makeMove : function(body) {

        var b = this.jsonToArray(JSON.stringify(body.board));
        var firstMove = body.firstMove;
        logger.debug("Game Board " + b + "FIRST MOVE: " + firstMove);

        if (firstMove) {
            b = this.initialMove(b);
        } else {
            b = this.block(b);
        }

        return b;
    },

    /**
     * 
     */
    findCoordinates : function(data) {
        for (var i = 0; i < 3; i++) {
            for (var j = 0; j < 3; j++) {
                if (!gameboard[i][j]) {
                    empty = true;
                }
            }
        }
    },

    /**
     * 
     */
    isWinner : function(gameboard) {

        var empty = false;

        // check for any empty cell
        for (var i = 0; i < 3; i++) {
            for (var j = 0; j < 3; j++) {
                if (!gameboard[i][j]) {
                    empty = true;
                }
            }
        }

        // check board vertically and horizontally
        for (var i = 0; i < 3; i++) {

            if (gameboard[i][0] && gameboard[i][0] == gameboard[i][1]
                    && gameboard[i][1] == gameboard[i][2]) {
                return gameboard[i][0];
            }
            if (gameboard[0][i] && gameboard[0][i] == gameboard[1][i]
                    && gameboard[1][i] == gameboard[2][i]) {
                return gameboard[0][i];
            }
        }

        // check board diagonally
        if (gameboard[0][0] && gameboard[0][0] == gameboard[1][1]
                && gameboard[1][1] == gameboard[2][2]) {
            return gameboard[0][0];

        }

        if (gameboard[0][2] && gameboard[0][2] == gameboard[1][1]
                && gameboard[1][1] == gameboard[2][0]) {
            return gameboard[0][2];
        }

        // no more empty cell - no winner
        if (!empty) {
            return 'tie';
        }
    }

};

logger.debug(BoardOperations);
module.exports = BoardOperations;
