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
    angular.extend(Gameboard, {'A1':'X', 'B1':'X', 'C1':'X'});
    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a row 2 win', function () {
    angular.extend(Gameboard, {'A2':'O', 'B2':'O', 'C2':'O'});
    expect(Gameboard.winner()).toBe('O');
  });

  it('should detect a row 3 win', function () {
    angular.extend(Gameboard, {'A3':'X', 'B3':'X', 'C3':'X'});
    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a col A win', function () {
    angular.extend(Gameboard, {'A1':'X', 'A2':'X', 'A3':'X'});
    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a col B win', function () {
    angular.extend(Gameboard, {'B1':'X', 'B2':'X', 'B3':'X'});
    expect(Gameboard.winner()).toBe('X');
  });

  it('should detect a col C win', function () {
    angular.extend(Gameboard, {'C1':'O', 'C2':'O', 'C3':'O'});
    expect(Gameboard.winner()).toBe('O');
  });

  it('should detect a col C win', function () {
    angular.extend(Gameboard, {'C1':'O', 'C2':'O', 'C3':'O'});
    expect(Gameboard.winner()).toBe('O');
  });

  it('should detect diagonal (from top left) win', function () {
    angular.extend(Gameboard, {'A1':'O', 'B2':'O', 'C3':'O'});
    expect(Gameboard.winner()).toBe('O');
  });

  it('should detect diagonal (from top right) win', function () {
    angular.extend(Gameboard, {'A3':'O', 'B2':'O', 'C1':'O'});
    expect(Gameboard.winner()).toBe('O');
  });

});
