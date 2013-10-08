'use strict';

angular.module('TicTacToeApp')
  .controller('MainCtrl', ['$scope', 'boardService', function ($scope, boardService) {
    $scope.Math = Math;
    $scope.displaySymbols = {
      O: '○',
      X: '×'
    };

    $scope.currentPlayer = 'X';

    $scope.nextPlayer = function () {
      $scope.currentPlayer = $scope.currentPlayer === 'X' ? 'O' : 'X';
    };

    $scope.processMove = function(move) {
      //make sure the tile is empty, otherwise turn is lost
      if ($scope.board.isTileEmpty(move.row, move.col)) {
        $scope.board.setMove(move.row, move.col, $scope.currentPlayer);
      }

      $scope.nextPlayer();
    };

    $scope.clickBoard = function (idx) {
      var row = Math.floor(idx / 3);
      var col = idx % 3;

      //don't accept clicks if tile isn't empty
      if ($scope.board.isTileEmpty(row, col)) {
        $scope.processMove({row: row, col: col});
      }
    };

    $scope.board = boardService.newBoard();
  }]);
