'use strict';

angular.module('ticTacToeApp') .service('Gameboard', function Gameboard() {


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

  this.reset = function() {
    var that = this;
    angular.forEach(['A', 'B', 'C'], function(col) {
      angular.forEach([1, 2, 3], function(row) {
        that[col + row] = '';
      });
    });
    this._turn = 'X';
    this.moves = 0;
    this.moveList = [];
  };

  this.winner = function() {
    var that = this;
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

    if (theWinnerIs === '') {
      var cellsUsed = 0;
      angular.forEach(['A', 'B', 'C'], function(col) {
        angular.forEach([1, 2, 3], function(row) {
          if (that[col + row] !== '') {
            cellsUsed++;
          }
        });
      });

      if (cellsUsed === 9) {
        theWinnerIs = 'D'; // draw
      }
    }


    return theWinnerIs;
  };

  this.play = function(cell) {
    if (this.winner() !== '') {
      return;
    }

    if (this[cell] === '') {
      this.moves++;
      this.moveList.push(cell);
      this[cell] = this._turn;
      this._turn = (this._turn === 'X') ? 'O' : 'X';
    } else {
      throw new Error('Cannot play the same cell twice');
    }
  };

  this.hypothetical = function(cell) {
    var h = angular.copy(this);
    h.play(cell);
    return h;
  };

  this.eachEmptyCell = function(f) {
    var that = this;

    angular.forEach(['A', 'B', 'C'], function(col) {
      angular.forEach([1, 2, 3], function(row) {
        var cell = col + row;
        if (that[cell] === '') {
          f(cell);
        }
      });
    });
  };

  this.toString = function() {
    var that = this;
    var buff = [];
    angular.forEach([1, 2, 3], function(row) {
      var rowBuff = [];
      angular.forEach(['A', 'B', 'C'], function(col) {
        var cell = col + row;
        rowBuff.push(that[cell] || ' ');
      });
      buff.push(rowBuff.join('|') + ((row === 1) ? ' ' + that.moveList.join('-') : ''));
    });

    return buff.join('\n-+-+-\n');

  };

  this.reset();
});
