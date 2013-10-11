angular.module('TicTacToeApp')
  .service('boardService', function () {
    'use strict';

    var Board = (function () {
      function Board() {
        if (!(this instanceof Board)) {
          return new Board();
        }

        this.n = 3;
        this.tiles = new Array(this.n * this.n);

        for (var i = 0; i < this.tiles.length; i++) {
          this.tiles[i] = '';
        }
      }

      Board.prototype.getMove = function getMoveAt(row, col) {
        return this.tiles[row * this.n + col];
      };

      Board.prototype.setMove = function getMoveAt(row, col, player) {
        this.tiles[row * this.n + col] = player;
      };

      Board.prototype.isTileEmpty = function isTileEmpty(row, col) {
        return this.getMove(row, col) === '';
      };

      Board.prototype.isBoardFull = function isBoardFull() {
        var foundEmptyTile = false;
        for (var i = 0; i < this.tiles.length; i++) {
          if (this.tiles[i] === '') {
            foundEmptyTile = true;
          }
        }
        return !foundEmptyTile;
      };

      Board.prototype.checkForWin = function() {
        var win, firstMove, i, j;
        for(i = 0; i < this.n; i++) {
          //check ith row
          win = true;
          firstMove = this.getMove(i, 0);
          for(j = 1; j < this.n; j++) {
            if (this.getMove(i, j) !== firstMove) {
              win = false;
            }
          }
          if (win && firstMove !== '') {
            return firstMove;
          }

          //check ith col
          win = true;
          firstMove = this.getMove(0, i);
          for(j = 1; j < this.n; j++) {
            if (this.getMove(j, i) !== firstMove) {
              win = false;
            }
          }
          if (win && firstMove !== '') {
            return firstMove;
          }
        }

        //check the diagonals
        win = true;
        firstMove = this.getMove(0, 0);
        for (i = 1; i < this.n; i++) {
          if (this.getMove(i, i) !== firstMove) {
            win = false;
          }
        }
        if (win && firstMove !== '') {
          return firstMove;
        }

        win = true;
        firstMove = this.getMove(0, this.n - 1);
        for (i = 1; i < this.n; i++) {
          if (this.getMove(i, this.n - 1 - i) !== firstMove) {
            win = false;
          }
        }
        if (win && firstMove !== '') {
          return firstMove;
        }

        return '';
      };

      return Board;
    })();

    return {
      Board: Board
    };
  });