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

    expect(Tictactoewinner.suggestMoveFor('O')).toBe('C1');
  });


  it('should suggest a move to block a row 2 win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    expect(Tictactoewinner.suggestMoveFor('X')).toBe('C2');

  });

  it('should suggest a move to block a row 3 win', function () {
    Gameboard.play('A2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B3'); // O
    expect(Tictactoewinner.suggestMoveFor('X')).toBe('C3');
  });

  it('should suggest a move to block a col A win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('A2'); // X
    expect(Tictactoewinner.suggestMoveFor('O')).toBe('A3');

  });

  it('should suggest a move to block a col B win', function () {
    Gameboard.play('B1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('B2'); // X

    expect(Tictactoewinner.suggestMoveFor('O')).toBe('B3');
  });

  it('should suggest a move to block a col C win', function () {
    Gameboard.play('C1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('C2'); // X
    expect(Tictactoewinner.suggestMoveFor('O')).toBe('C3');

  });


  it('should suggest a move to block a diagonal (from top left) win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    expect(Tictactoewinner.suggestMoveFor('O')).toBe('C3');
  });

  it('should suggest a move to block a diagonal (from top right) win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    expect(Tictactoewinner.suggestMoveFor('O')).toBe('C1');
  });


});
