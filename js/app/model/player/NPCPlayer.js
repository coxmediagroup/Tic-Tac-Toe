define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.Model.extend({
        defaults: {
            isCurrent: false,
            playerName: 'Computer',
            playerType: 'NPC'
        },

        VALUES: {
            PC: {
                '2': -1000 ,
                '1': -10,
                '0': -1
            },
            NPC: {
                '2': 1000 ,
                '1': 10,
                '0': 1
            }
        },

        TWO_CELL_MODIFIER_NPC: 10,
        ONE_CELL_MODIFIER_NPC: 1,
        EMPTY_CELL_MODIFIER: 0,
        LOSING_BOARD_SCORE: -1000,
        TWO_CELL_MODIFIER_PC: -10,
        ONE_CELL_MODIFIER_PC: -1,

        simulate: function(gameState) {
            var bestMove = this.bestPossibleMove(gameState);
            gameState.unset('boardState', {silent: true});
            gameState.set('boardState', bestMove);
        },

        bestPossibleMove: function(gameState) {
            var currentBoardState = gameState.get('boardState');
            var bestBoard = undefined;
            var bestScore = this.calculateBoardScore(currentBoardState);

            _.each(currentBoardState, function(row, rowIndex) {
                _.each(row, function(col, colIndex) {
                    if (col === 0) {
                        var newBoard = [];
                        _.each(currentBoardState.slice(), function(rows) {
                             newBoard.push(rows.slice());
                        });
                        newBoard[rowIndex][colIndex] = gameState.get('computer').get('playerType');
                        var newScore = this.calculateBoardScore(newBoard);
                        if (newScore <= bestScore || bestBoard === undefined) {
                            bestBoard = newBoard;
                            bestScore = newScore;
                        }
                    }
                }, this);
            }, this);

            return bestBoard;
        },

        calculateBoardScore: function(board) {
            var score = 0;

            _.each(board, function(row, index, rowArray){
                var rowScore = 0;
                var lastCol = 0;
                var colAlike = 0;
                _.each(row, function(col, colIndex, colArray) {
                    if (col !== 0) {
                        if (col === lastCol) {
                            colAlike++;
                            rowScore = this.VALUES[col][colAlike.toString()];
                        } else {
                            rowScore += this.VALUES[col]['1'];
                            lastCol = col;
                        }
                    }
                }, this);
                score += rowScore;
            }, this);

            for (var i = 0; i < 3; ++i) {
                var colScore = 0;
                var lastCol = 0;
                var colAlike = 0;
                for (var j = 0; j < 3; ++j) {
                    if (board[j][i] !== 0) {
                        if (board[j][i] === lastCol) {
                            colAlike++;
                            colScore = this.VALUES[board[j][i]][colAlike.toString()];
                        } else {
                            colScore += this.VALUES[board[j][i]]['1'];
                            lastCol = board[j][i];
                        }
                    }
                }
                score += colScore;
            }
            var diagnonalScore = 0;
            for (var j = 0; j < 3; ++j) {
                var lastCol = 0;
                if (board[j][j] !== 0) {
                    if (board[j][j] === lastCol) {
                        colAlike++;
                        diagnonalScore = this.VALUES[board[j][j]][colAlike.toString()];
                    } else {
                        diagnonalScore += this.VALUES[board[j][j]]['1'];
                        lastCol = board[j][j];
                    }
                }
            }

            score += diagnonalScore;
            diagnonalScore = 0;
            for (var i = 2, j = 0; i >= 0; --i, j++) {
                var lastCol = 0;
                if (board[i][j] !== 0) {
                    if (board[i][j] === lastCol) {
                        colAlike++;
                        diagnonalScore = this.VALUES[board[i][j]][colAlike.toString()];
                    } else {
                        diagnonalScore += this.VALUES[board[i][j]]['1'];
                        lastCol = board[i][j];
                    }
                }
            }

            score += diagnonalScore;

            return score;
        }
    });
});