'use strict';

angular.module('ticTacToeApp').service('Tictactoewinner', ['Gameboard', 
      function Tictactoewinner(Gameboard) {
  
  var sequences = angular.copy(Gameboard.WINNING_SEQUENCES);


  this.suggestMoveFor = function(player) {
    var mustBlock = [];
    var opponent = (player === 'X') ? 'O': 'X';

    angular.forEach(sequences, function(seq) {

      var count = 0;
      angular.forEach(seq, function(cell) {
        if (Gameboard[cell] === opponent) {
          count++;
        }
      });

      if (count === 2) {
        angular.forEach(seq, function(cell) {
          if (Gameboard[cell] !== opponent) {
            mustBlock.push(cell);
          }
        });
      }
    });

    if (mustBlock.length > 0) {
      return mustBlock[0];
    }


    return '';
  };




}]);
