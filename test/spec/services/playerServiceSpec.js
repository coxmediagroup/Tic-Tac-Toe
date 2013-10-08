'use strict';

describe('Service: playerService - ', function () {
  var service, brdService;

  beforeEach(function() {
    module('TicTacToeApp');
    inject(function(playerService, boardService) {
      service = playerService;
      brdService = boardService;
    });
  });

  it('Interactive player should always return undefined.', function () {
    var board = brdService.newBoard();
    var player = service.newInteractivePlayer();
    expect(player.move(board)).toBeUndefined();
  });

  it('Easy AI should always pick the next open tile.', function () {
    var idxToRowCol = function(idx) {
      return {
        row: Math.floor(idx / 3),
        col: idx % 3
      }
    };

    var board = brdService.newBoard();
    var player = service.newEasyAiPlayer();
    expect(player.move(board)).toEqual(idxToRowCol(0));

    board.setMove(0, 0, 'X');
    board.setMove(0, 1, 'X');
    board.setMove(1, 0, 'X');
    board.setMove(1, 1, 'X');

    expect(player.move(board)).toEqual(idxToRowCol(2));
  });

});