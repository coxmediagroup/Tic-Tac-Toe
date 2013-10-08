'use strict';

angular.module('TicTacToeApp')
  .controller('MainCtrl', ['$scope', 'boardService', function ($scope, boardService) {
    $scope.board = boardService.newBoard();
  }]);
