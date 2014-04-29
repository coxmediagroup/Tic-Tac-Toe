'use strict';

angular.module('ticTacToeApp').factory('continueGame', function() {
  return {
    gameSoFar:window.game_so_far || [],
    player:window.player || 'X'
  }
});
