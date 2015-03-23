'use strict';

angular.module('tictactoe')
    .config(function($stateProvider){
        $stateProvider
            .state('instructions', {
                url: '/instructions',
                templateUrl: 'app/instructions/instructions.html',
                controller: 'InstructionsCtrl'
            });
    });