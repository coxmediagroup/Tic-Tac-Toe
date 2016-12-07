angular.module('TicTacToeApp')
  .service('playerService', ['boardService', function (boardService) {
    'use strict';
    /*
     Players have one function

     move(Board) - returns an object specifying the row, col
     of the move. Alternatively, undefined can be returned to
     tell the game to wait for user action. Example:

     {row: 1, col: 2}
     */

    //This player will always wait for clicks.
    var InteractivePlayer = (function () {
      function InteractivePlayer() {
        if (!(this instanceof InteractivePlayer)) {
          return new InteractivePlayer();
        }
      }

      InteractivePlayer.prototype.move = function move() {
        //don't return anything, the game will wait for a click on the board
      };

      return InteractivePlayer;
    })();

    //A dumb computer player.
    var EasyAiPlayer = (function () {
      function EasyAiPlayer() {
        if (!(this instanceof EasyAiPlayer)) {
          return new EasyAiPlayer();
        }
      }

      EasyAiPlayer.prototype.move = function move(board) {
        //implement a simple algorithm to get game flow going.
        //currently picks the next open tile  :)
        for (var i = 0; i < 9; i++) {
          var row = Math.floor(i / 3);
          var col = i % 3;
          if (board.isTileEmpty(row, col)) {
            return {
              row: row,
              col: col
            };
          }
        }
      };

      return EasyAiPlayer;
    })();

    //An implementation of n-ply Minimax.
    //scoring is done by number of available win scenarios,
    //negated for other player. Winning boards are scored 10.
    var MinimaxAiPlayer = (function () {
      function MinimaxAiPlayer() {
        if (!(this instanceof MinimaxAiPlayer)) {
          return new MinimaxAiPlayer();
        }
      }

      MinimaxAiPlayer.prototype.scoreBoard = function scoreBoard(board, player) {
        function isMineOrEmpty (c) {
          return c === '' || c === player;
        }
        var win = board.checkForWin();
        if(win) {
          if(win === player) {
            return 10;
          } else {
            return -10;
          }
        }
        var score = 0; //the number of ways left to win
        var canWin, i, j;
        for (i = 0; i < board.n; i++) {
          //check ith row
          canWin = true;
          for (j = 0; j < board.n; j++) {
            if (!isMineOrEmpty(board.getMove(i, j))) {
              canWin = false;
            }
          }
          if (canWin) {
            score = score + 1;
          }

          //check ith col
          canWin = true;
          for (j = 0; j < board.n; j++) {
            if (!isMineOrEmpty(board.getMove(j, i))) {
              canWin = false;
            }
          }
          if (canWin) {
            score = score + 1;
          }
        }

        //check the diagonals
        canWin = true;
        for (i = 0; i < board.n; i++) {
          if (!isMineOrEmpty(board.getMove(i, i))) {
            canWin = false;
          }
        }
        if (canWin) {
          score = score + 1;
        }

        canWin = true;
        for (i = 0; i < board.n; i++) {
          if (!isMineOrEmpty(board.getMove(i, board.n - 1 - i))) {
            canWin = false;
          }
        }
        if (canWin) {
          score = score + 1;
        }

        return score;
      };

      MinimaxAiPlayer.prototype.move = function move(board, player) {
        var MAX_DEPTH = 5; //examine at most half the game
        var scoreBoard = this.scoreBoard;

        function otherPlayer(player) {
          return player === 'X' ? 'O' : 'X';
        }

        function idxToMove(idx) {
          return {
            row: Math.floor(idx / 3),
            col: idx % 3
          };
        }

        //my move - want to maximize
        function maxValue(board, depth) {
          if(board.isBoardFull() || depth >= MAX_DEPTH) {
            var score = scoreBoard(board, player);
            return {utility: score};
          }

          var maxUtil = {
            utility: -100,
            move: {}
          };

          for (var i = 0; i < board.tiles.length; i++) {
            var testMove = idxToMove(i);
            if(board.isTileEmpty(testMove.row, testMove.col)) {
              board.setMove(testMove.row, testMove.col, player); //test move

              var util = minValue(board, depth + 1);
              if (util.utility > maxUtil.utility) {
                maxUtil.utility = util.utility;
                maxUtil.move = testMove;
              }

              board.setMove(testMove.row, testMove.col, ''); //unset move
            }
          }
          return maxUtil;
        }

        //other player's move
        function minValue(board, depth) {
          if(board.isBoardFull() || depth >= MAX_DEPTH) {
            var score = -scoreBoard(board, otherPlayer(player));
            return {utility: score};
          }

          var minUtil = {
            utility: 100,
            move: {}
          };

          for (var i = 0; i < board.tiles.length; i++) {
            var testMove = idxToMove(i);
            if(board.isTileEmpty(testMove.row, testMove.col)) {
              board.setMove(testMove.row, testMove.col, otherPlayer(player)); //test move

              var util = maxValue(board, depth + 1);
              if (util.utility < minUtil.utility) {
                minUtil.utility = util.utility;
                minUtil.move = testMove;
              }

              board.setMove(testMove.row, testMove.col, ''); //unset move
            }
          }
          return minUtil;
        }


        var testBoard = new boardService.Board();
        testBoard.tiles = board.tiles.slice(0, board.tiles.length);

        var utility = maxValue(testBoard, 0);

        return utility.move;
      };

      return MinimaxAiPlayer;
    })();

    return {
      InteractivePlayer: InteractivePlayer,
      EasyAiPlayer: EasyAiPlayer,
      MinimaxAiPlayer: MinimaxAiPlayer
    };
  }]);