angular.module('tttApp', ['ngResource', 'ngRoute']);

angular.module('tttApp').config(function ($routeProvider, $locationProvider) {

    $locationProvider.html5Mode(true);

    $routeProvider.when('/home', {
        templateUrl: '/partials/default/landing',
        controller: 'tttLandingCtrl'
    });

    $routeProvider.when('/basicgame', {
        templateUrl: '/partials/game/basicgame',
        controller: 'tttBasicGameCtrl'
    });
});

angular.module('tttApp').run(function ($rootScope, $location) {
    $rootScope.$on('$routeChangeError', function (evt, current, previous, rejection) {
        Console.log(evt);
    })
});