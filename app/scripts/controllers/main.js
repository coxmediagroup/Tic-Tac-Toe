'use strict';

angular.module('TicTacToeApp')
  .controller('MainCtrl', ['$scope', 'boardService', 'playerService', function ($scope, boardService, playerService) {
    $scope.Math = Math;
    $scope.displaySymbols = {
      O: '○',
      X: '×'
    };

    $scope.board = new boardService.Board();
    $scope.currentPlayer = '';
    $scope.status = 'Waiting to start game';
    $scope.players = {};
    $scope.gameInProgress = false;

    $scope.startGame = function () {
      $scope.board = new boardService.Board();
      $scope.players.X = new playerService.InteractivePlayer();
      $scope.players.O = new playerService.EasyAiPlayer();
      $scope.currentPlayer = 'X';
      $scope.gameInProgress = true;
      $scope.checkGameStatus();
    };

    $scope.endGame = function () {
      $scope.gameInProgress = false;
      $scope.currentPlayer = '';
    };

    $scope.nextPlayer = function () {
      $scope.currentPlayer = $scope.currentPlayer === 'X' ? 'O' : 'X';
      $scope.checkGameStatus();
    };

    $scope.processMove = function (move) {
      //make sure the tile is empty, otherwise turn is lost
      if ($scope.board.isTileEmpty(move.row, move.col)) {
        $scope.board.setMove(move.row, move.col, $scope.currentPlayer);
      }

      $scope.nextPlayer();
    };

    $scope.clickBoard = function (idx) {
      if (!$scope.gameInProgress) {
        return;
      }

      if ($scope.waitForClick) {
        var row = Math.floor(idx / 3);
        var col = idx % 3;

        //don't accept clicks if tile isn't empty
        if ($scope.board.isTileEmpty(row, col)) {
          $scope.processMove({row: row, col: col});
        }
      }
    };

    $scope.checkGameStatus = function () {
      //check for game winner
      //if not, a full board is a tie
      var winner = $scope.board.checkForWin();
      if (winner) {
        $scope.endGame();
        $scope.status = 'Game Over: ' + $scope.displaySymbols[winner] + ' wins!';
      } else if ($scope.board.isBoardFull()) {
        $scope.endGame();
        $scope.status = 'Game Over: Tie';
      } else {
        $scope.status = $scope.displaySymbols[$scope.currentPlayer] + '\' turn';
      }
    };

    $scope.$watch('currentPlayer', function () {
      if (!$scope.gameInProgress) {
        return;
      }

      var move = $scope.players[$scope.currentPlayer].move($scope.board);
      console.log('Player move');
      console.log(move);

      if (!move) {
        //no move was returned, wait for clicks on the board
        $scope.waitForClick = true;
      } else {
        //set the move
        $scope.waitForClick = false;
        $scope.processMove(move);
      }
    });

    $scope.endGame();
  }]);
