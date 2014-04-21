var tictactoe = angular.module('tictactoe', []);

tictactoe.config([
    '$httpProvider',
    '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
        $httpProvider.defaults.transformRequest = function(data) {
            if (data === undefined) {
                return data;
            }
            return $.param(data);
        };
    }
]);

tictactoe.controller('TicTacToeCtrl', ['$scope', '$http', '$element', function($scope, $http, $element) {

    $scope.makeMove = function(row, col) {
        var data = {
                'row': row,
                'col': col
            },
            el = '#move_' + row + col;

        $http.post('/makemove/', data)
            .success(function(data, status, headers, config) {
                $element.find(el).prop('disabled', true).html('X');
                console.log('success');
                // TODO: Check the following in data:
                // if player won
                // else if ai won
            })
            .error(function(data, status, headers, config) {
                console.log('error');
            });
    };
}]);