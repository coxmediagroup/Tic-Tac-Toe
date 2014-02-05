'use strict';
/* App Controllers */

var GameApp = angular.module('GameApp', []);

GameApp.factory('game', function() {
    return new Game();
});


GameApp.controller('GameCtrl', function GameCtrl($scope, game) {
    $scope.game = game;
    $scope.whoStart = "human";
    $scope.humanMarker = "O";
    $scope.startGame = function(){
        var humanMarker = $scope.humanMarker,
            computerMarker = humanMarker === "O" ? "X" : "O";
        $scope.h = new Human(humanMarker);
        $scope.c = new Computer(computerMarker);
        game.initialize();
        if ($scope.whoStart === "computer"){
            $scope.message = game.MESSAGE_COMPUTER_TURN;
            $scope.c.move(game,true);
            $scope.message = game.MESSAGE_HUMAN_TURN;
        }
        else{
            $scope.message = game.MESSAGE_HUMAN_TURN;
        }
    };

    $scope.humanTryingMove = function(position){
        if (game.isValidMove(position)){
            $scope.h.move(game,position);
            if (game.is_game_over()){
                if (game.winner === '-')
                    $scope.message = "Game over with Draw";
                else
                    $scope.message = game.MESSAGE_WON;
            }
            else{
                $scope.c.move(game);
                if (game.is_game_over()){
                    if (game.winner === '-')
                        $scope.message = "Game over with Draw";
                    else
                        $scope.message = game.MESSAGE_MISS;
                }
            }
        }
    }

    $scope.startGame();
});

