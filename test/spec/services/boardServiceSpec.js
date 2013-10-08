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

    it('should be able to determine if a tile is empty', function() {
      var board = service.newBoard();
      expect(board.isTileEmpty(1, 1)).toEqual(true);
      board.setMove(1, 1, 'X');
      expect(board.isTileEmpty(1, 1)).toEqual(false);
    })

    it('should be able to determine if every tile is taken', function() {
      var board = service.newBoard();
      expect(board.isBoardFull()).toEqual(false);

      for(var i = 0; i < board.tiles.length; i++) {
        board.tiles[i] = 'X';
      }

      expect(board.isBoardFull()).toEqual(true);
    })
  });
});