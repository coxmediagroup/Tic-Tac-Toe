'use strict';

angular.module('tictactoe')
    .controller('GameCtrl', ['$scope', 'Stats', 'Game', function($scope, Stats, Game){
        var pieces = Game.pieces();

        $scope.statistics = Stats.getStats() || [];
        $scope.spaceNumbers = [0,1,2,3,4,5,6,7,8];

        function aiMoves(){
            var aiTurn = Game.aiTurn();

            if(aiTurn.space > -1) {
                $scope['space' + aiTurn.space] = pieces.ai;

                if (aiTurn.hasWon) {
                    $scope.winner = 'AI wins!';
                    Stats.addStats({ winner: 'ai' });
                    updateStats();
                }
            } else {
                $scope.winner = 'Tie Game!';
                Stats.addStats({ winner: 'tie' });
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

        };

        $scope.spaceClicked = function(which){
            if(Game.canMove(which)) {
                $scope['space' + which] = pieces.player;
                if(Game.checkMove(which)){
                    $scope.winner = 'Human wins!';
                    Stats.addStats({ winner: 'user' });
                    updateStats();
                } else {
                    aiMoves();
                }
            }
        }
    }]);