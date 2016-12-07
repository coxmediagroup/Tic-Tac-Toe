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
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    }
]);

tictactoe.controller('TicTacToeCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
    $scope.makeMove = function() {
        var move = {'move': $scope.move};
        $scope.letter = 'O';

        $http.post('/makemove/', move)
            .success(function(data, status, headers, config) {
                if (data.success) {
                    if (data.move !== undefined) {
                        $timeout(function() {
                            // Mark AI move
                            markMove(data.move, 'X');
                        }, 300);
                    }

                    if (data.win_status) {
                        var alert = angular.element('.alert-box');
                        alert.addClass('alert alert-success');

                        if (data.win_status === 'tie') {
                            alert.append("It's a tie. You almost got me that time!");
                        } else {
                            data.board.map(function(letter, i) {
                                if (letter === '') {
                                    markMove(i, '');
                                }
                            });
                            if (data.win_status === 'computer') {
                                alert.append('I win. Better luck next time!');
                            } else {
                                // This should never happen
                                alert.append("You won! Oops I don't know how that happened!");
                            }
                        }
                        alert.append(' Click on the links above to play again.');
                    }
                }
            })
            .error(function(data, status, headers, config) {
                console.log('error');
            });
    };

    function markMove(move, letter) {
        var el = '#move_' + move,
            model = angular.element(el).scope();

        model.letter = letter;
        model.btn_state = true;
    }
}]);
