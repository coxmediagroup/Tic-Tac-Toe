'use strict';

describe('Service: boardService', function () {
  var service;

  beforeEach(function () {
    module('TicTacToeApp');
    inject(function (boardService) {
      service = boardService;
    });
  });

  it('should return an object capable of creating a Tic-Tac-Toe board.', function () {
    var board = new service.Board();
    expect(Array.isArray(board.tiles)).toEqual(true);
    expect(board.tiles.length).toEqual(9);
  });

  describe('A Board', function () {
    it('should be able to get and set moves.', function () {
      var board = new service.Board();
      expect(board.getMove(1, 1)).toEqual('');
      board.setMove(1, 1, 'X');
      expect(board.getMove(1, 1)).toEqual('X');
    });

    it('should be able to determine if a tile is empty', function () {
      var board = new service.Board();
      expect(board.isTileEmpty(1, 1)).toEqual(true);
      board.setMove(1, 1, 'X');
      expect(board.isTileEmpty(1, 1)).toEqual(false);
    });

    it('should be able to determine if every tile is taken', function () {
      var board = new service.Board();
      expect(board.isBoardFull()).toEqual(false);

      for (var i = 0; i < board.tiles.length; i++) {
        board.tiles[i] = 'X';
      }

      expect(board.isBoardFull()).toEqual(true);
    });

    it('should be able to determine a winner across a row', function() {
      var board = new service.Board();
      board.setMove(2, 0, 'X');
      board.setMove(2, 1, 'X');
      board.setMove(2, 2, 'X');
      expect(board.checkForWin()).toEqual('X');
    });

    it('should be able to determine a winner down a column', function() {
      var board = new service.Board();
      board.setMove(0, 1, 'O');
      board.setMove(1, 1, 'O');
      board.setMove(2, 1, 'O');
      expect(board.checkForWin()).toEqual('O');
    });

    it('should be able to determine a winner for top-left diagonal', function() {
      var board = new service.Board();
      board.setMove(0, 0, 'O');
      board.setMove(1, 1, 'O');
      board.setMove(2, 2, 'O');
      expect(board.checkForWin()).toEqual('O');
    });

    it('should be able to determine a winner for top-right diagonal', function() {
      var board = new service.Board();
      board.setMove(0, 2, 'X');
      board.setMove(1, 1, 'X');
      board.setMove(2, 0, 'X');
      expect(board.checkForWin()).toEqual('X');
    });
  });
});