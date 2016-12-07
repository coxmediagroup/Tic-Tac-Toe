'use strict';

angular.module('ticTacToeApp')
.controller('MainCtrl', 
[ 
'$scope', 'Gameboard', 'TicTacToeWinner', '$timeout', 'continueGame', 'currentSite', '$http', 'csrf',
function ($scope, Gameboard, TicTacToeWinner, $timeout, continueGame, currentSite, $http, csrf) {

  $scope.rows = [1, 2, 3];
  $scope.cols = ['A', 'B', 'C'];
  $scope.board = Gameboard;
  $scope.xy = '';
  $scope.opponent = '';
  $scope.canStartGame = true;
  $scope.winner = '';
  $scope.neverStarted = true;
  $scope.youWon = false;
  $scope.draw = false;
  $scope.youLost = false;
  $scope.wins = 0;
  $scope.losses = 0;
  $scope.draws = 0;

  $scope.makePermalink = function() {
    if (!currentSite.domain || Gameboard.moveList.length === 0) {
      $scope.permalink = '#';
      return;
    }
    var u = currentSite.domain;
    if (u.charAt(u.length-1) !== '/') {
      u += '/';
    }

    u += '' + $scope.xy + '-' + Gameboard.moveList.join('-') + '/';
    if (u.substring(0, 4) !== 'http') {
      u = 'http://' + u;
    }

    $scope.permalink = u;

  };

  $scope.wopr = function() {
    Gameboard.reset();
    $scope.winner = '';
    $scope.neverStarted = false;

    var turnTime = 750;
    var maxTime = 20000;
    var startTime = (new Date()).getTime();
    var turn = 'X';

    // disable normal turns
    var normalPlayTurn = $scope.playTurn;
    var normalPermalink = $scope.makePermalink;
    $scope.makePermalink = angular.noop;

    $scope.playTurn = angular.noop;

    var playWopr = function () {
      var t = (new Date()).getTime() - startTime;

      if ($scope.winner) {
        turn = 'X';
        Gameboard.reset();
        $scope.winner = '';

        if (t >= maxTime) {
          $scope.playTurn = normalPlayTurn;
          $scope.makePermalink = normalPermalink;
          return;
        }

      } else {
        Gameboard.play(TicTacToeWinner.suggestMoveFor(turn));
        turn = (turn === 'X') ? 'O' : 'X';
      }

      $scope.winner = Gameboard.winner();

      if (turnTime > 25) {
        turnTime -= 25;
      }
      $timeout(playWopr, turnTime);
    };

    playWopr();

  };


  $scope.playTurn = function(cell) {
    if ($scope.winner) {
      return;
    }

    try {
      Gameboard.play(cell);
      $scope.makePermalink();
    } catch (e) {
      // cell already played
      return;
    }
    $scope.winner = Gameboard.winner();
    if (!$scope.winner) {
      Gameboard.play(TicTacToeWinner.suggestMoveFor($scope.opponent));
      $scope.winner = Gameboard.winner();
      $scope.makePermalink();
    }
  };

  $scope.startGame = function(xy) {
    $scope.neverStarted = false;

    Gameboard.reset();

    $scope.xy = xy;
    $scope.winner = '';
    $scope.canStartGame = false;
    $scope.opponent = (xy === 'X') ? 'O' : 'X';

    if ($scope.opponent === 'X') {
      Gameboard.play(TicTacToeWinner.suggestMoveFor($scope.opponent));
    }
    $scope.makePermalink();
  };



  $scope.$watch('winner', function(winner) {
    if (winner) {
      $scope.canStartGame = true;
      $scope.youWon = winner === $scope.xy;
      $scope.draw = winner === 'D';
      $scope.youLost = winner === $scope.opponent;

      if ($scope.youLost) {
        $scope.losses += 1;
      }
      if ($scope.youWon) {
        $scope.wins += 1;
      }
      if ($scope.draw) {
        $scope.draws += 1;
      }

    }
  });

  $scope.$watch('permalink', function() {
    if ($scope.permalink && $scope.permalink !== '#') {
      $http.post($scope.permalink);
    }
  });

  if (continueGame.gameSoFar.length > 0) {
    $scope.neverStarted = false;
    Gameboard.reset();
    $scope.xy = continueGame.player;
    $scope.winner = '';
    $scope.canStartGame = false;
    $scope.opponent = ($scope.xy === 'X') ? 'O' : 'X';

    var turn = 'X';
    angular.forEach(continueGame.gameSoFar, function(move) {
      try {
        Gameboard.play(move)
        turn = (turn === 'X') ? 'O' : 'X';
      } catch(e) {}
    });

    if (turn === $scope.opponent) {
      Gameboard.play(TicTacToeWinner.suggestMoveFor($scope.opponent));
    }
    $scope.makePermalink();

  }


}]);

