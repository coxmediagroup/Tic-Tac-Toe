'use strict';

angular.module('tictactoe')
    .controller('GameCtrl', ['$scope', 'Stats', 'Game', function($scope, Stats, Game){
        var pieces = Game.pieces();

        function aiMoves(){
            var aiTurn = Game.aiTurn();

            if(aiTurn.space > -1) {
                $scope['space' + aiTurn.space] = pieces.ai;

                if (aiTurn.hasWon) {
                    $scope.winner = 'AI wins!';
                }
            } else {
                $scope.winner = 'Tie Game!';
            }
        }

        $scope.spaceNumbers = [0,1,2,3,4,5,6,7,8];

        $scope.spaceClicked = function(which){
            if(Game.canMove(which)) {
                $scope['space' + which] = pieces.player;
                if(Game.checkMove(which)){
                    $scope.winner = 'Player wins!';
                } else {
                    aiMoves();
                }
            }
        }
    }]);