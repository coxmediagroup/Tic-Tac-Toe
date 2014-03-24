'use strict';


// Declare app level module which depends on filters, and services
var myApp = angular.module('myApp', [ 'myApp.directives'])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

        // Set primary route
        $routeProvider.when('/tic-tac-toe', {templateUrl: 'partials/_board'});

        // Fallback
        $routeProvider.otherwise({redirectTo: '/tic-tac-toe'});
    }]
    )
