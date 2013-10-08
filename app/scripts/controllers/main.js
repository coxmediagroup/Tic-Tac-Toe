'use strict';

angular.module('TicTacToeApp')
  .controller('MainCtrl', ['$scope', 'boardService', 'playerService', function ($scope, boardService, playerService) {
    $scope.Math = Math;
    $scope.displaySymbols = {
      O: '○',
      X: '×'
    };

    $scope.currentPlayer = 'X';
    $scope.players = {};
    $scope.players.X = playerService.newInteractivePlayer();
    $scope.players.O = playerService.newEasyAiPlayer();

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
      if($scope.waitForClick) {
        var row = Math.floor(idx / 3);
        var col = idx % 3;

        //don't accept clicks if tile isn't empty
        if ($scope.board.isTileEmpty(row, col)) {
          $scope.processMove({row: row, col: col});
        }
      }
    };

    $scope.$watch('currentPlayer', function() {
      var move = $scope.players[$scope.currentPlayer].move($scope.board);
      console.log('Player move');
      console.log(move);

      if(!move) {
        //no move was returned, wait for clicks on the board
        $scope.waitForClick = true;
      } else {
        //set the move
        $scope.waitForClick = false;
        $scope.processMove(move);
      }
    });

    $scope.board = boardService.newBoard();
  }]);
