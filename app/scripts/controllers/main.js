'use strict';

angular.module('TicTacToeApp')
  .controller('MainCtrl', ['$scope', 'TicTacToeBoard', function ($scope, TicTacToeBoard) {
    $scope.board = TicTacToeBoard;
    
    // determines when a new row starts
    $scope.newRow = function(idx) {
      return idx%$scope.board.width===0;
    };
    
    // determines when a row ends.
    $scope.endRow = function(idx) {
      return (idx+1)%$scope.board.width===0;
    };
    
    // selects a square to be played
    $scope.select = function(block) {
      if($scope.board.select(block)) {
        $scope.board.aiMove();
      }
    };
    
    // resets the game board
    $scope.reset = function() {
      $scope.board.resetBoard();
    };
    
  }]);
