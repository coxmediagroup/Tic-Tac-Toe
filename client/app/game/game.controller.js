'use strict';

angular.module('tictactoe')
    .controller('GameCtrl', ['$scope', 'Stats', 'Game', '$interval', function($scope, Stats, Game, $interval){
        var pieces = Game.pieces();

        $scope.statistics = Stats.getStats() || [];
        $scope.spaceNumbers = [0,1,2,3,4,5,6,7,8];

        function aiMoves(){
            var aiTurn = Game.aiTurn();

            if(aiTurn.space > -1) {
                $scope['space' + aiTurn.space] = pieces.ai;

                if (aiTurn.hasWon) {
                    $scope.winner = 'AI wins!';
                    Stats.addStats({ winner: 'ai', moves: Game.getMoves() });
                    updateStats();
                }
            } else {
                $scope.winner = 'Tie Game!';
                Stats.addStats({ winner: 'tie', moves: Game.getMoves() });
                updateStats();
            }
        }

        function updateStats(){
            $scope.statistics = Stats.getStats() || [];
        }

        $scope.newGame = function(){
            var c;

            Game.newGame();

            for(c = 0; c < $scope.spaceNumbers.length; c++){
                $scope['space' + c] = '';
            }

            $scope.winner = '';
        };

        $scope.spaceClicked = function(which){
            if(Game.canMove(which)) {
                $scope['space' + which] = pieces.player;
                Game.addMove('user', which);
                if(Game.checkMove(which)){
                    $scope.winner = 'Human wins!';
                    Stats.addStats({ winner: 'user', moves: Game.getMoves() });
                    updateStats();
                } else {
                    aiMoves();
                }
            }
        };

        $scope.replay = function(which){
            var moves = angular.copy($scope.statistics[which].moves),
                counter,
                move;

            // change
            $scope.newGame();

            counter = $interval(function(){
                if(moves.length){
                    move = moves.shift();
                    if(move[0] === 'a'){
                        // X or O
                        $scope['space' + move[1]] = 'O';
                    } else {
                        $scope['space' + move[1]] = 'X';
                    }
                } else {
                    $interval.cancel(counter);
                }
            }, 1000);
        }
    }]);












