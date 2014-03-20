'use strict';

angular.module('ticTacToeApp').service('Tictactoewinner', ['Gameboard', 
      function Tictactoewinner(Gameboard) {
  
  var sequences = {};
  sequences['X'] = angular.copy(Gameboard.WINNING_SEQUENCES);
  sequences['O'] = angular.copy(Gameboard.WINNING_SEQUENCES);


  this.defend = function(player) {
    var mustBlock = [];
    var opponent = (player === 'X') ? 'O': 'X';

    angular.forEach(sequences[player], function(seq) {

      var count = 0;
      angular.forEach(seq, function(cell) {
        if (Gameboard[cell] === opponent) {
          count++;
        }
      });

      if (count === 2) {
        angular.forEach(seq, function(cell) {
          if (Gameboard[cell] === '') {
            mustBlock.push(cell);
          }
        });
      }
    });

    if (mustBlock.length > 0) {
      return mustBlock[0];
    }

  };

  this.attack = function(player) {
    var opponent = (player === 'X') ? 'O': 'X';

    var punt = '';
    angular.forEach(['A', 'B', 'C'], function(col) {
      angular.forEach([1, 2, 3], function(row) {
        var cell = col + row;
        if (!punt && Gameboard[cell] === '') {
          punt = cell;
        }
      });
    });

    // if 1st move, alter the sequence order to try a new plan
    if (Gameboard.moves <= 1) {
      var first = sequences[player].shift();
      sequences[player].push(first);
    }

    var sequenceThatCanWin;
    angular.forEach(sequences[player], function(seq) {
      if (sequenceThatCanWin) return;

      var opponentOccupied = false;
      angular.forEach(sequences[player], function(cell) {
        if (!opponentOccupied && Gameboard[cell] === opponent) {
          opponentOccupied = true;
        }
      });

      if (!opponentOccupied) {
        sequenceThatCanWin = seq;
      }
    });

    var schemedMove = '';
    angular.forEach([0, 2, 1], function(cellIndex) {
      var cell = sequenceThatCanWin[cellIndex];
      if (!schemedMove && Gameboard[cell] === '') {
        schemedMove = cell;
      }      
    });

    return schemedMove || punt;
  };

  this.suggestMoveFor = function(player) {
    return this.defend(player) || this.attack(player);
  };




}]);
