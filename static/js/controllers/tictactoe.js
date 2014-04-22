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

    $scope.makeMove = function(mv) {
        var move = {'move': mv};

        // Player move
        markMove(mv, 'O');
        $http.post('/makemove/', move)
            .success(function(data, status, headers, config) {
                if (data.success) {
                    setTimeout(function() {
                        // AI move
                        markMove(data.move, 'X');
                    }, 4000);
                    console.log(data);
                    // TODO: Check the following in data:
                    // if player won
                    // else if ai won
                }
                // else Something went wrong
            })
            .error(function(data, status, headers, config) {
                console.log('error');
            });
    };

    function markMove(move, letter) {
        var el = '#move_' + move;
        $element.find(el).prop('disabled', true).html(letter);
    }
}]);
