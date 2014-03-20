'use strict';

describe('Service: Gameboard', function () {

  // load the service's module
  beforeEach(module('ticTacToeApp'));

  // instantiate service
  var Gameboard;
  beforeEach(inject(function (_Gameboard_) {
    Gameboard = _Gameboard_;
  }));

  it('should have 9 blank cells', function () {
    expect(Gameboard.A1).toBe('');
    expect(Gameboard.B1).toBe('');
    expect(Gameboard.C1).toBe('');
    expect(Gameboard.A2).toBe('');
    expect(Gameboard.B2).toBe('');
    expect(Gameboard.C2).toBe('');
    expect(Gameboard.A3).toBe('');
    expect(Gameboard.B3).toBe('');
    expect(Gameboard.C3).toBe('');
  });

  it('should start with no winner', function () {
    expect(!!Gameboard.winner()).toBe(false);
  });

  it('should detect a row 1 win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('C1'); // X

    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a row 2 win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    Gameboard.play('C1'); // X
    Gameboard.play('C2'); // O

    expect(Gameboard.winner()).toBe('O');
  });

  it('should detect a row 3 win', function () {
    Gameboard.play('A2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('C1'); // X
    Gameboard.play('C3'); // O
    expect(Gameboard.winner()).toBe('O');
  });

  it('should detect a col A win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('A2'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('A3'); // X

    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a col B win', function () {
    Gameboard.play('B1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('B2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('B3'); // X

    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a col C win', function () {
    Gameboard.play('C1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('C2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('C3'); // X

    expect(Gameboard.winner()).toBe('X');
  });


  it('should detect diagonal (from top left) win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('C3'); // X
    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect diagonal (from top right) win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('C1'); // X
    expect(Gameboard.winner()).toBe('X');
  });

  it('should throw an exception if we try and play the same cell twice', function() {
    Gameboard.play('B2');
    expect(function() {Gameboard.play('B2')}).toThrow(new Error('Cannot play the same cell twice'));
  });

  it('should register a win when taking turns with the play() method', function() {
    Gameboard.play('A1'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    Gameboard.play('B3'); // X
    Gameboard.play('C2'); // O
    expect(Gameboard.winner()).toBe('O');
  });

  it('play() method should be a no-op, once we\'ve won', function() {
    Gameboard.play('A1'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    Gameboard.play('B3'); // X
    Gameboard.play('C2'); // O
    expect(Gameboard.winner()).toBe('O');
    Gameboard.play('C1'); // X would win, but O already did
    expect(Gameboard.C1).toBe('');    
    expect(Gameboard.winner()).toBe('O');
  });

  it('should work if we play(), win, reset(), play() and win', function() {
    Gameboard.play('A1'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    Gameboard.play('B3'); // X
    Gameboard.play('C2'); // O
    expect(Gameboard.winner()).toBe('O');
    
    Gameboard.reset();
    
    Gameboard.play('C1'); // should be X again, and we can play
    expect(Gameboard.C1).toBe('X');    
    expect(Gameboard.winner()).toBe('');

    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    Gameboard.play('B3'); // X
    Gameboard.play('C2'); // O

    expect(Gameboard.winner()).toBe('O');


  });


  it('should detect a draw', function() {
    Gameboard.play('B2'); // X
    Gameboard.play('C2'); // O
    Gameboard.play('C3'); // X
    Gameboard.play('A1'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('A3'); // X
    Gameboard.play('C1'); // O
    Gameboard.play('A2'); // X

    expect(Gameboard.winner()).toBe('D');
  });

  it('should count moves', function() {
    expect(Gameboard.moves).toBe(0);
    Gameboard.play('B2'); // X
    expect(Gameboard.moves).toBe(1);
    Gameboard.play('C2'); // O
    expect(Gameboard.moves).toBe(2);
  });

  it('should reset move count on reset()', function() {
    expect(Gameboard.moves).toBe(0);
    Gameboard.play('B2'); // X
    expect(Gameboard.moves).toBe(1);
    Gameboard.reset();
    expect(Gameboard.moves).toBe(0);
  });
});
