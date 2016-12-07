var app = angular.module('TicTacToeApp', [])

app.controller('TicTacToeCtrl',
    ['$scope', '$http',
    function($scope, $http){

        var getBoardState = function(){
            return [[null,null,null],[null,null,null],[null,null,null]];
        }

        $scope.winner = null;
        $scope.gameOver = false;
        $scope.tie = false;
        $scope.humansTurn = true;
        $scope.board = getBoardState();
        $scope.updateBoard = function($event){
            if($scope.gameOver){
                return;
            }
            if($scope.humansTurn){
                var x = $event.target.dataset.x;
                var y = $event.target.dataset.y;
                if($scope.board[y][x] === null){
                    $scope.board[y][x] = 'X';
                    $scope.humansTurn = false;
                    $http({
                        method: 'GET',
                        url: '/api/omove',
                        params: {
                            'board': JSON.stringify($scope.board)
                        }
                    }).success(function(data, status, headers, config){
                        var gameResult = data.result;
                        if(gameResult.gameOver){
                            $scope.winner = gameResult.winner;
                            $scope.tie = gameResult.winner === null;
                            $scope.gameOver = true;
                        }
                        var move = data.move;
                        if(move !== null){
                            $scope.board[move[1]][move[0]] = 'O';
                        }
                        $scope.humansTurn = true;
                    }).error(function(data, status, headers, config){
                        alert("error getting next move");
                    });
                }
            }
        }



    }
]);
