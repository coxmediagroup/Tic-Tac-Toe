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
  })
});