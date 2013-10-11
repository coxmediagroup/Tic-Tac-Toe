'use strict';

describe('Service: playerService - ', function () {
  var service, brdService;

  beforeEach(function () {
    module('TicTacToeApp');
    inject(function (playerService, boardService) {
      service = playerService;
      brdService = boardService;
    });
  });

  it('Interactive player should always return undefined.', function () {
    var board = new brdService.Board();
    var player = new service.InteractivePlayer();
    expect(player.move(board)).toBeUndefined();
  });

  it('Easy AI should always pick the next open tile.', function () {
    var idxToRowCol = function (idx) {
      return {
        row: Math.floor(idx / 3),
        col: idx % 3
      }
    };

    var board = new brdService.Board();
    var player = new service.EasyAiPlayer();
    expect(player.move(board)).toEqual(idxToRowCol(0));

    board.setMove(0, 0, 'X');
    board.setMove(0, 1, 'X');
    board.setMove(1, 0, 'X');
    board.setMove(1, 1, 'X');

    expect(player.move(board)).toEqual(idxToRowCol(2));
  });


  describe('MinimaxAiPlayer', function() {
    it('should be able to score an empty board', function() {
      var board = new brdService.Board();
      var player = new service.MinimaxAiPlayer();

      expect(player.scoreBoard(board, 'X')).toEqual(8);
    });

    it('should be able to score a board with center same player', function() {
      var board = new brdService.Board();
      board.setMove(1, 1, 'X');
      var player = new service.MinimaxAiPlayer();

      expect(player.scoreBoard(board, 'X')).toEqual(8);
    });

    it('should be able to score a board with center other player', function() {
      var board = new brdService.Board();
      board.setMove(1, 1, 'O');
      var player = new service.MinimaxAiPlayer();

      expect(player.scoreBoard(board, 'X')).toEqual(4);
    });

    it('should be able to score a board with only 1 diag open', function() {
      var board = new brdService.Board();
      board.setMove(0, 1, 'O');
      board.setMove(0, 2, 'O');
      board.setMove(1, 0, 'O');
      board.setMove(1, 2, 'O');
      board.setMove(2, 0, 'O');
      board.setMove(2, 1, 'O');
      var player = new service.MinimaxAiPlayer();

      expect(player.scoreBoard(board, 'X')).toEqual(1);
    });

    it('should be able to score board1 correctly', function() {
      var player = new service.MinimaxAiPlayer();
      var board = new brdService.Board();
      board.tiles = ['O', 'X', '', '', '', 'X', '', '', ''];
      expect(player.scoreBoard(board, 'O')).toEqual(4);
    });

    it('should be able to score board2 correctly', function() {
      var player = new service.MinimaxAiPlayer();
      var board = new brdService.Board();
      board.tiles = ['X', 'O', 'X', '', '', '', '', '', ''];
      expect(player.scoreBoard(board, 'O')).toEqual(3);
    });

  })

});