angular.module('TicTacToeApp').service('playerService', [function () {
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
    }

    InteractivePlayer.prototype.move = function move() {
      //don't return anything, the game will wait for a click on the board
    };

    return InteractivePlayer;
  })();

  //A dumb computer player.
  var EasyAiPlayer = (function () {
    function EasyAiPlayer() {
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

  return {
    newInteractivePlayer: function () {
      return new InteractivePlayer();
    },
    newEasyAiPlayer: function () {
      return new EasyAiPlayer();
    }
  };
}]);