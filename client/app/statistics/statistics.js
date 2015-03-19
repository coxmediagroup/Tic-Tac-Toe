'use strict';

angular.module('tictactoe')
    .config(function($stateProvider){
        $stateProvider
            .state('statistics', {
                url: '/statistics',
                templateUrl: 'app/statistics/statistics.html',
                controller: 'StatsCtrl'
            });
    });