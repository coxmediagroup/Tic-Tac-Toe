angular.module('TicTacToeApp')
  .service('boardService', function () {
    'use strict';

    var Board = (function () {
      function Board() {
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

      return Board;
    })();

    return {
      newBoard: function () {
        return new Board();
      }
    };
  });