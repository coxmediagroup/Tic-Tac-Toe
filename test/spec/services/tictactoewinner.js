'use strict';

describe('Service: Tictactoewinner', function () {

  // load the service's module
  beforeEach(module('ticTacToeApp'));

  // instantiate service
  var Tictactoewinner;
  var Gameboard;
  beforeEach(inject(function (_Tictactoewinner_) {
    Tictactoewinner = _Tictactoewinner_;
  }));

  beforeEach(inject(function (_Gameboard_) {
    Gameboard = _Gameboard_;
  }));

  it('should suggest a move to block a row 1 win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X

    expect(Tictactoewinner.defend('O')).toBe('C1');
  });


  it('should suggest a move to block a row 2 win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    expect(Tictactoewinner.defend('X')).toBe('C2');

  });

  it('should suggest a move to block a row 3 win', function () {
    Gameboard.play('A2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B3'); // O
    expect(Tictactoewinner.defend('X')).toBe('C3');
  });

  it('should suggest a move to block a col A win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('A2'); // X
    expect(Tictactoewinner.defend('O')).toBe('A3');

  });

  it('should suggest a move to block a col B win', function () {
    Gameboard.play('B1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('B2'); // X

    expect(Tictactoewinner.defend('O')).toBe('B3');
  });

  it('should suggest a move to block a col C win', function () {
    Gameboard.play('C1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('C2'); // X
    expect(Tictactoewinner.defend('O')).toBe('C3');

  });


  it('should suggest a move to block a diagonal (from top left) win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    expect(Tictactoewinner.defend('O')).toBe('C3');
  });

  it('should suggest a move to block a diagonal (from top right) win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    expect(Tictactoewinner.defend('O')).toBe('C1');
  });

  it('should always win or draw as X if player is unwise', function () {
    for (var i = 0; i < Gameboard.WINNING_SEQUENCES.length; i++) {
      var unwiseMoves = ['A1', 'B3', 'C2', 'C1', 'B2', 'A3', 'C3', 'A2', 'B1'];
      while(unwiseMoves.length > 0) {
        // let computer go first (X)
        Gameboard.play(Tictactoewinner.suggestMoveFor('X'));
        expect(Gameboard.winner()).not.toBe('O');

        var move;
        while (unwiseMoves.length > 0) {
          move = unwiseMoves.shift();
          if (Gameboard[move] === '') {
            break;
          }
          move = '';
        }

        if (move) {
          Gameboard.play(move);
          expect(Gameboard.winner()).not.toBe('O');
        }

        if (Gameboard.winner() !== '') {
          break;
        }

      }

    }

  });

  it('should always win or draw as O if player is unwise', function () {
    for (var i = 0; i < Gameboard.WINNING_SEQUENCES.length; i++) {
      var unwiseMoves = ['A1', 'B3', 'C2', 'C1', 'B2', 'A3', 'C3', 'A2', 'B1'];
      var movesTaken = [];
      while(unwiseMoves.length > 0) {
        // let player go first (X)
        expect(Gameboard.winner()).not.toBe('O');

        var move;
        while (unwiseMoves.length > 0) {
          move = unwiseMoves.shift();
          if (Gameboard[move] === '') {
            break;
          }
          move = '';
        }

        if (move) {
          Gameboard.play(move);
          movesTaken.push(move);
          if (Gameboard.winner()) break;
        }

        Gameboard.play(Tictactoewinner.suggestMoveFor('O'));
        

        if (Gameboard.winner() !== '') {
          break;
        }

      }
      if (Gameboard.winner() === 'X') {
        console.debug('Unexpected win!\n' + movesTaken.join(', ') + '\n' + Gameboard.toString());
      }

      expect(Gameboard.winner()).not.toBe('X');

      Gameboard.reset();
    }

  });

  it('should always draw against itself', function () {
    for (var i = 0; i < Gameboard.WINNING_SEQUENCES.length; i++) {
      while (!Gameboard.winner()) {        
        Gameboard.play(Tictactoewinner.suggestMoveFor('X'));
        if (Gameboard.winner()) break;
        Gameboard.play(Tictactoewinner.suggestMoveFor('O'));

      }
      expect(Gameboard.winner()).toBe('D');
      Gameboard.reset();

    }
  });
});
