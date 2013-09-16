define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.Model.extend({
        defaults: {
            isCurrent: false,
            playerName: 'Computer',
            playerType: 'NPC',
            isWinner: false
        },

        VALUES: {
            PC: {
                '3': -1000 ,
                '2': -10,
                '1': -1
            },
            NPC: {
                '3': 1000 ,
                '2': 10,
                '1': 1
            }
        },

        simulate: function(gameState) {
            var simulationState = gameState.clone();
            simulationState.set('boardState', gameState.cloneBoard());
            simulationState.set('currentPlayer', gameState.get('currentPlayer'));
            simulationState.set('computer', gameState.get('computer'));
            simulationState.set('player', gameState.get('player'));

            var bestMove = this.bestPossibleMove(simulationState, 2).bestBoard; //only look ahead one move.
            gameState.unset('boardState', {silent: true});
            gameState.set('boardState', bestMove);
        },

        generateBoardsList: function(gameState) {
            var currentBoardState = gameState.get('boardState');
            var boardsList = [];

            if (gameState.gameHasWinner()) {
                return boardsList;
            }

            _.each(currentBoardState, function (row, rowIndex) {
                _.each(row, function (col, colIndex) {
                    if (col === 0) {
                        var newBoard = gameState.cloneBoard();
                        newBoard[rowIndex][colIndex] = gameState.get('currentPlayer').get('playerType');
                        boardsList.push(newBoard);
                    }
                }, this);
            }, this);

            return boardsList;
        },

        bestPossibleMove: function(gameState, depth) {
            var boards = this.generateBoardsList(gameState);
            var turnType = gameState.get('currentPlayer').get('playerType');
            var bestScore = turnType === 'NPC' ? -1000000 : 1000000;     //effectively +infinity to -infinity
            var currentBoardScore = 0;
            var bestBoard = undefined;

            if (depth === 0 || boards.length === 0) {
                bestScore = this.calculateBoardScore(gameState.get('boardState'));
                bestBoard = gameState.get('boardState');
            } else {
                for (var i = 0; i < boards.length; ++i) {
                    if (turnType === 'NPC') {
                        gameState.set('currentPlayer', gameState.get('player'));
                        gameState.set('boardState', boards[i]);
                        currentBoardScore = this.bestPossibleMove(gameState, depth - 1).bestScore;
                        if (currentBoardScore > bestScore) {
                            bestScore = currentBoardScore;
                            bestBoard = boards[i];
                        }
                    } else {
                        gameState.set('currentPlayer', gameState.get('computer'));
                        gameState.set('boardState', boards[i]);
                        currentBoardScore = this.bestPossibleMove(gameState, depth - 1).bestScore;
                        if (currentBoardScore < bestScore) {
                            bestScore = currentBoardScore;
                            bestBoard = boards[i];
                        }
                    }
                }
            }

            return { bestBoard: bestBoard, bestScore: bestScore };
        },

        calculateBoardScore: function(board) {
            var score = 0;

            for (var q = 0; q < 3; q++) {
                var colScore = 0;
                var lastCol1 = 0;
                var colAlike = 0;
                for (var l = 0; l < 3; l++) {
                    if (board[q][l] !== 0) {
                        if (board[q][l] === lastCol1) {
                            colAlike++;
                            colScore = this.VALUES[board[q][l]][colAlike.toString()];
                        } else if (colAlike > 0) {
                            colScore = 0;
                            break;
                        } else {
                            colScore += this.VALUES[board[q][l]]['1'];
                            colAlike++;
                            lastCol1 = board[q][l];
                        }
                    }
                }
                score += colScore;
            }

            for (var k = 0; k < 3; ++k) {
                var colScore = 0;
                var lastCol1 = 0;
                var colAlike = 0;
                for (var m = 0; m < 3; ++m) {
                    if (board[m][k] !== 0) {
                        if (board[m][k] === lastCol1) {
                            colAlike++;
                            colScore = this.VALUES[board[m][k]][colAlike.toString()];
                        } else if (colAlike > 0) {
                            colScore = 0;
                            break;
                        } else {
                            colScore += this.VALUES[board[m][k]]['1'];
                            colAlike++;
                            lastCol1 = board[m][k];
                        }
                    }
                }
                score += colScore;
            }


            var diagnonalScore = 0;
            for (var j = 0; j < 3; ++j) {
                var lastCol2 = 0;
                var colAlike = 0;
                if (board[j][j] !== 0) {
                    if (board[j][j] === lastCol2) {
                        colAlike++;
                        diagnonalScore = this.VALUES[board[j][j]][colAlike.toString()];
                    } else if (colAlike > 0) {
                        diagnonalScore = 0;
                        break;
                    } else {
                        diagnonalScore += this.VALUES[board[j][j]]['1'];
                        colAlike++;
                        lastCol2 = board[j][j];
                    }
                }
            }

            score += diagnonalScore;
            diagnonalScore = 0;
            for (var i = 2, n = 0; i >= 0; --i, n++) {
                var lastCol3 = 0;
                var colAlike = 0;
                if (board[i][n] !== 0) {
                    if (board[i][n] === lastCol3) {
                        colAlike++;
                        diagnonalScore = this.VALUES[board[i][n]][colAlike.toString()];
                    } else if (colAlike > 0) {
                        diagnonalScore = 0;
                        break;
                    } else {
                        diagnonalScore += this.VALUES[board[i][n]]['1'];
                        colAlike++;
                        lastCol3 = board[i][n];
                    }
                }
            }

            score += diagnonalScore;

            return score;
        }
    });
});