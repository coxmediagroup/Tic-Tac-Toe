'use strict';

// Strategy based on http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
// Newell and Simon's 1972 tic-tac-toe program
// Kevin Crowley, Robert S. Siegler (1993). 
// "Flexible Strategy Use in Young Children’s Tic-Tac-Toe".
// Cognitive Science 17 (4): 531–561. doi:10.1016/0364-0213(93)90003-Q

angular.module('ticTacToeApp').service('TicTacToeWinner', ['Gameboard',
      function Tictactoewinner(Gameboard) {
  
  var OPPOSITE_CORNERS = {
    'A1':'C3',
    'C3':'A1',
    'C1':'A3',
    'A3':'C1'
  };


  this.defend = function(player, returnAll, board) {
    var mustBlock = [];
    var opponent = (player === 'X') ? 'O': 'X';
    board = board || Gameboard;

    angular.forEach(Gameboard.WINNING_SEQUENCES, function(seq) {

      var count = 0;
      angular.forEach(seq, function(cell) {
        if (board[cell] === opponent) {
          count++;
        }
      });

      if (count === 2) {
        angular.forEach(seq, function(cell) {
          if (board[cell] === '') {
            mustBlock.push(cell);
          }
        });
      }
    });

    if (returnAll) {
      return mustBlock;
    } else if (mustBlock.length) {
      return mustBlock[0];
    } else {
      return '';
    }

  };


  this.winningMove = function(player) {
    var move = '';
    angular.forEach(Gameboard.WINNING_SEQUENCES, function(seq) {

      var count = 0;
      angular.forEach(seq, function(cell) {
        if (Gameboard[cell] === player) {
          count++;
        }
      });

      if (count === 2) {
        angular.forEach(seq, function(cell) {
          if (Gameboard[cell] === '') {
            move = cell;
          }
        });
      }
    });

    return move;
  };

  this.punt = function() {
    var move = '';
    Gameboard.eachEmptyCell(function(cell) {
      move = cell;
    });
    return move;
  };

  this.forkOpponent = function(player) {
    var that = this;
    var opponent = (player === 'X') ? 'O' : 'X';
    var move = '';
    Gameboard.eachEmptyCell(function(cell) {
      var afterMove = Gameboard.hypothetical(cell);
      var defend = that.defend(opponent, true, afterMove);
      if (defend.length > 1) {
        move = cell;
      }
    });
    return move;
  };

  this.blockFork = function(player, logit) {
    var that = this;
    var move = '';
    var forks = [];
    var foundForks = {};

    Gameboard.eachEmptyCell(function(move1) {
      var after1 = Gameboard.hypothetical(move1);
      after1.eachEmptyCell(function(move2) {
        var after2 = after1.hypothetical(move2);
        var defend = that.defend(player, true, after2);
        if (defend.length > 1 && !foundForks[move2]) {
          forks.push(move2);
          foundForks[move2] = 1;
        }
      });
    });

    if (logit) console.info('forks detected', forks, foundForks);
    if (forks.length === 1) {
      move = forks[0];
    } else if (forks.length > 1) {
      // if there is than one move that could cause a fork
      // then try and divert the player by going on the offensive


      angular.forEach(Gameboard.WINNING_SEQUENCES, function(seq) {
        if (move) {
          return; // we found a move, stop trying
        }
        var emptyCount = 0;
        var playerCount = 0;


        angular.forEach(seq, function(cell) {
          if (Gameboard[cell] === player) {
            playerCount++;
          } else if (Gameboard[cell] === '') {
            emptyCount++;
          }
        });

        // this might work, lets make sure the other player
        // has to play an unforkable cell to block this win
        if (playerCount === 1 && emptyCount === 2) {
  
          if (logit) console.info('trying counter offensive', seq.join('-'));

          // what cells could we take?
          var possibilites = [];


          // first get 2 empties
          angular.forEach(seq, function(cell) {
            if (Gameboard[cell] === '') {
              possibilites.push(cell);
            }
          });

          if (logit) console.log('possibilites', possibilites);

          if (!foundForks[possibilites[0]] && !foundForks[possibilites[1]]) {
            move = possibilites[0];
          } else if (foundForks[possibilites[0]] && !foundForks[possibilites[1]]) {
            move = possibilites[0];
          } else if (!foundForks[possibilites[0]] && foundForks[possibilites[1]]) {
            move = possibilites[1];
          }

        }

      });



    }

    return move;
  };

  this.takeCenterIfWeCan = function() {
    if (Gameboard.B2 === '') {
      return 'B2';
    } else {
      return '';
    }
  };

  this.takeAnOppositeCorner = function(player) {
    var opponent = (player === 'X') ? 'O' : 'X';
    var move = '';
    angular.forEach(OPPOSITE_CORNERS, function(opp, corner) {
      if (Gameboard[opp] === opponent && Gameboard[corner] === '') {
        move = corner;
      }
    });
    return move;
  };

  this.takeAnyCorner = function() {
    var move = '';
    angular.forEach(OPPOSITE_CORNERS, function(opp, corner) {
      if (Gameboard[corner] === '') {
        move = corner;
      }
    });
    return move;
  };

  this.takeAnySide = function() {
    var move = '';
    angular.forEach(['A2', 'B1', 'C2', 'B3'], function(side) {
      if (Gameboard[side] === '') {
        move = side;
      }
    });
    return move;
  };

  this.openingMoveForO = function() {
    // if X didn't take center, take it
    if (Gameboard['B2'] !== 'X') {
      return 'B2';
    } else {
      return ['A1', 'A3', 'C1', 'C3'][Math.floor(Math.random() * 4)];
    }
  };

  this.suggestMoveFor = function(player) {

    if (player === 'X' || Gameboard.moves > 1) {
      return (this.winningMove(player) ||
        this.defend(player) ||
        this.forkOpponent(player) ||
        this.blockFork(player) ||
        this.takeCenterIfWeCan(player) ||
        this.takeAnOppositeCorner(player) ||
        this.takeAnyCorner(player) ||
        this.takeAnySide(player) ||
        this.punt());

    } else { // first move for O

      return this.openingMoveForO() || this.punt();



    }
  };




}]);
