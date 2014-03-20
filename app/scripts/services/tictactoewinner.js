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
    var consideredSequenceDesireability = 0;
    var goingToTryCenter = false;

    angular.forEach(sequences[player], function(seq) {
      var opponentOccupied = false;
      angular.forEach(seq, function(cell) {
        if (!opponentOccupied && Gameboard[cell] === opponent) {
          opponentOccupied = true;
        }
      });

      if (!opponentOccupied) {
        var desirablity = 0;
        var triesCenter = false;
        angular.forEach(seq, function(cell) {
          if (Gameboard[cell] === player) {
            desirablity++;
          }

          // favor schemes including center
          if (cell === 'B2') {
            desirablity += 3;
            triesCenter = true;
          }

          // favor schemes with corners
          if (cell === 'A1' || cell === 'A3' || cell === 'C1' || cell === 'C3') {
            desirablity++;
          }

        });



        if (!sequenceThatCanWin || (desirablity > consideredSequenceDesireability)) {
          sequenceThatCanWin = seq;
          consideredSequenceDesireability = desirablity;
          goingToTryCenter = triesCenter;
        }
      }
    });

    var schemedMove = '';

    // go for the center!! 
    if (goingToTryCenter && !Gameboard['B2']) return 'B2';

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
