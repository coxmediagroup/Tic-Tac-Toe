'use strict';

/* Controllers */

angular.module('simple-games.controllers', []).
  controller('TicTacToeController', function ($scope, $http, $location) {
    
    $scope.message = "Pick your sign";
    
    $scope.makeMove = function ( index ) {
      $http.get('/tictactoe/move/' + index + "/").then(function(response) {
            $scope.squares = response.data[0].board;
            $scope.message = response.data[0].message;
            if( !response.data[0].status ) { 
              $scope.makeMove = null;
              $scope.message = null;
              $scope.winner = response.data[0].winner;
            }
        });
    };

    $scope.setGame = function ( sign ) {
      $http.get('/tictactoe/new/' + sign + "/").then(function(response) {
            $('.sign-block').unbind().remove();
            $scope.squares = response.data[0].board;
            $scope.message = response.data[0].message; 
        });
    };
  }).
  controller('loginController', function ( $scope, $location ) {    
    $scope.games = ['tictactoe'];
    $scope.goGame = function(game) {
      $("#goGameForm").attr("action", game + "/").submit();
    };
});