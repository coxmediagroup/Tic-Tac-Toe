'use strict';

angular.module('tictactoe')
    .controller('GameCtrl', ['$scope', 'Stats', 'Game', '$interval', function($scope, Stats, Game, $interval){
        var pieces = Game.pieces();

        $scope.statistics = Stats.getStats() || [];
        $scope.spaceNumbers = [0,1,2,3,4,5,6,7,8];

        /*
         *
         */
        function aiMoves(){
            var aiTurn = Game.aiTurn();

            if(aiTurn.space > -1) {
                $scope['space' + aiTurn.space] = pieces.ai;

                if (aiTurn.hasWon) {
                    $scope.winner = 'AI wins!';
                    Stats.addStats({ winner: 'ai', moves: Game.getMoves() });
                    updateStats();
                }
            }

            if(aiTurn.finished || aiTurn.space === -1){
                $scope.winner = 'Tie Game!';
                Stats.addStats({ winner: 'tie', moves: Game.getMoves() });
                updateStats();
            }
        }

        /*
         * Update statistics in view
         */
        function updateStats(){
            $scope.statistics = Stats.getStats() || [];
        }

        /*
         * Clear Grid
         */
        function clearGrid(){
            var c;

            for(c = 0; c < $scope.spaceNumbers.length; c++){
                $scope['space' + c] = '';
            }

            $scope.winner = '';
        }

        /*
         * Reset the game
         */
        $scope.resetGame = function(){
            clearGrid();

            Game.newGame();

            if(!Game.getUserFirst()){
                aiMoves();
            }
        };

        /*
         * Handles clicks on Tic-Tac-Toe grid
         *
         * @param {Number} space Which space is clicked
         */
        $scope.spaceClicked = function(space){
            if(Game.canMove(space)) {
                $scope['space' + space] = pieces.player;
                Game.addMove('u', space);
                if(Game.checkMove(space)){
                    $scope.winner = 'User wins!';
                    Stats.addStats({ winner: 'user', moves: Game.getMoves() });
                    updateStats();
                } else {
                    aiMoves();
                }
            }
        };

        /*
         * Replays previous games
         * 
         * Make a 
         *
         * @param {Number} which Which game was selected to replay
         */
        $scope.replay = function(which){
            console.log(which);
            var moves = angular.copy($scope.statistics[which].moves),
                counter,
                move,
                x = true;

            clearGrid();

            // emulate a real game with a 1s timeout and place pieces on the grid
            counter = $interval(function(){
                if(moves.length){
                    move = moves.shift();
                    $scope['space' + move[1]] = x ? 'X' : 'O';
                    x = !x;
                } else {
                    $interval.cancel(counter);
                }
            }, 1000);
        }
    }]);












