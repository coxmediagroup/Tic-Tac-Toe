'use strict';

angular.module('ticTacToeApp') .service('Gameboard', function Gameboard() {
  var that = this;

  this.WINNING_SEQUENCES = [
    // row wins
    ['A1', 'B1', 'C1'],
    ['A2', 'B2', 'C2'],
    ['A3', 'B3', 'C3'],

    // col wins
    ['A1', 'A2', 'A3'],
    ['B1', 'B2', 'B3'],
    ['C1', 'C2', 'C3'],

    // diagonal wins
    ['A1', 'B2', 'C3'],
    ['A3', 'B2', 'C1']
  ];

  angular.forEach(['A', 'B', 'C'], function(col) {
    angular.forEach([1, 2, 3], function(row) {
      that[col + row] = '';

    });
  });

  this.winner = function() {
    var theWinnerIs = '';
    angular.forEach(['X', 'O'], function(player) {
      angular.forEach(that.WINNING_SEQUENCES, function(seq) {
        var count = 0;
        angular.forEach(seq, function(cell) {
          if (that[cell] === player) {
            count++;
          }
        });

        if (count === 3) {
          theWinnerIs = player;
        }
      });
    });
    return theWinnerIs;
  };

});
