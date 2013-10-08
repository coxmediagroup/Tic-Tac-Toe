'use strict';

angular.module('TicTacToeApp')
  .controller('MainCtrl', ['$scope', 'boardService', function ($scope, boardService) {
    $scope.Math = Math;
    $scope.displaySymbols = {
      O: '○',
      X: '×'
    };

    $scope.board = boardService.newBoard();
    $scope.board.setMove(0, 0, 'X');
    $scope.board.setMove(1, 1, 'O');
    $scope.board.setMove(2, 2, 'X');
  }]);
