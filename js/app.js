'use strict';
/* App Controllers */

var GameApp = angular.module('GameApp', []);

GameApp.factory('game', function() {
    return new Game();
});


GameApp.controller('GameCtrl', function GameCtrl($scope, game) {
    $scope.game = game;
    $scope.whoStart = "human";
    $scope.startGame = function(){
        $scope.c = new Computer('X');
        $scope.h = new Human('O');
        game.initialize();
        if ($scope.whoStart === "computer"){
            $scope.message = game.MESSAGE_COMPUTER_TURN;
            $scope.c.move(game);
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

