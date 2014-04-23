'use strict';


var CLIENT_ID = '74921937461';

var SCOPE = 'https://www.googleapis.com/auth/userinfo.email';

var app = angular.module('tictactoe', []);

function init() {
  window.init();
}

app.controller('GameCtrl', function($scope, $window) {

  $window.init = function() {
    $scope.$apply(function() {
      $scope.auth(true);
    });
  }

  $scope.auth = function(immediate) {
    var params = {
      client_id: CLIENT_ID,
      scope: SCOPE,
      immediate: immediate
    };
    gapi.auth.authorize(params, function(result) {
      if (result && !result.error) {
        $scope.authorized = true;
        $scope.$apply();
        $scope.load();
      } else {
        document.querySelector('button').style.display = 'block';
      }
    });
  };

  var updateGame = function(response) {
    $scope.game = response;
    $scope.$apply();
  };

  var isSquareOccupied = function(square) {
    return square.className == 'X' || square.className == 'O';
  };

  var isGameOver = function() {
    return !!$scope.game.outcome;
  };

  $scope.load = function() {
    gapi.client.load('tictactoe', 'v1', function() {
      $scope.loaded = true;
      $scope.start();
    }, '/_ah/api');
  };

  $scope.start = function() {
    gapi.client.tictactoe.start().execute(updateGame);
  }

  $scope.move = function(clickEvent) {
    var square = clickEvent.target;
    if (isGameOver() || isSquareOccupied(square))
      return;
    var message = {id: $scope.game.id, square: square.id};
    gapi.client.tictactoe.move(message).execute(updateGame);
  };

  $scope.replay = function() {
    var message = {id: $scope.game.id};
    gapi.client.tictactoe.replay(message).execute(updateGame);
  };

});
