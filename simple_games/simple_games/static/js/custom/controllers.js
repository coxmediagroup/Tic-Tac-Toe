'use strict';

/* Controllers */

angular.module('simple-games.controllers', []).
  controller('TicTacToeController', function ($scope, $http, $location) {
    
    function drawBoard( squares, message ) {
      for (var i = 0; i < squares.length; i++) {
        if (!$(".game .board li:eq("+i+")").hasClass(squares[i])) {
          $(".game .board li:eq("+i+")").addClass(squares[i]);
        }
      };
      $scope.message = message;
    };
    $('.board').hide();
    $scope.message = "Pick your sign";
    
    $scope.makeMove = function( move ){
      $http.get('/tictactoe/move/' + move + "/").then(function(response) {

            var squares = response.data[0].board;
            var message = response.data[0].message;
            drawBoard(squares, message);

            if( !response.data[0].status ) { 
              $scope.makeMove = null;
              
              $scope.message = null;
              $scope.winner = response.data[0].winner;
            }
        });
    };
    
    $scope.setGame = function( sign ) {
      $http.get('/tictactoe/new/' + sign + "/").then(function(response) {
            $('.sign-block').unbind().remove();
            $('.board').show();
            var squares = response.data[0].board;
            var message = response.data[0].message;
            drawBoard(squares, message);
        });
    };
  }).
  controller('loginController', function ($scope, $location) {
    $scope.games = ['tictactoe'];

    $scope.goGame = function(game) {
      $("#goGameForm").attr("action", game + "/").submit();
    };
});