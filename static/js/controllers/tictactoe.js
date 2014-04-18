var tictactoe = angular.module('tictactoe', []);

tictactoe.config([
    '$httpProvider',
    '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    }
]);

tictactoe.controller('TicTacToeCtrl', ['$scope', '$http', function($scope, $http, _) {

    $scope.makeMove = function(row, col) {
        var data = {};

        $http.post('/makemove/', data)
            .success(function(data, status, headers, config) {
                console.log('success');
            })
            .error(function(data, status, headers, config) {
                console.log('error');
            });
    };
}]);