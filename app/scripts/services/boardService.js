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

      return Board;
    })();

    return {
      newBoard: function () {
        return new Board();
      }
    };
  });