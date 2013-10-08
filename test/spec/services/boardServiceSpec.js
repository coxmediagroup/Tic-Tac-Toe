'use strict';

describe('Service: boardService', function () {
  var service;

  beforeEach(function() {
    module('TicTacToeApp');
    inject(function(boardService) {
      service = boardService;
    });
  });

  it('should return an object capable of creating a Tic-Tac-Toe board.', function () {
    var board = service.newBoard();
    expect(Array.isArray(board.tiles)).toEqual(true);
    expect(board.tiles.length).toEqual(9);
  });

  describe('A Board', function() {
    it('should be able to get and set moves.', function() {
      var board = service.newBoard();
      expect(board.getMove(1, 1)).toEqual('');
      board.setMove(1, 1, 'X');
      expect(board.getMove(1, 1)).toEqual('X');
    });
  });
});