'use strict';

angular.module('tictactoe', ['ui.router'])
    .config(function($locationProvider, $urlRouterProvider){
        $urlRouterProvider.otherwise('/');
        $locationProvider.html5Mode(true);
    });