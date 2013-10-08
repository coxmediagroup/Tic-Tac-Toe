angular.module('TicTacToeApp')
  .service('boardService', function () {
    'use strict';

    var Board = (function () {
      function Board() {
        if (!(this instanceof Board)) {
          return new Board();
        }

        this.tiles = new Array(9);

        for (var i = 0; i < this.tiles.length; i++) {
          this.tiles[i] = '';
        }
      }

      Board.prototype.getMove = function getMoveAt(row, col) {
        return this.tiles[row * 3 + col];
      };

      Board.prototype.setMove = function getMoveAt(row, col, player) {
        this.tiles[row * 3 + col] = player;
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

      return Board;
    })();

    return {
      Board: Board
    };
  });