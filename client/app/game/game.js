'use strict';

angular.module('tictactoe')
    .config(function($stateProvider){
        $stateProvider
            .state('play', {
                url: '/',
                templateUrl: 'app/game/game.html',
                controller: 'GameCtrl'
            });
    });