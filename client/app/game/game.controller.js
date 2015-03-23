'use strict';

/*
 * Game controller
 *
 * Contains interaction between the game logic (Game service) and game view
 */
angular.module('tictactoe')
    .controller('GameCtrl', ['$scope', 'Stats', 'Game', '$interval', function($scope, Stats, Game, $interval){

        // setup first game
        var pieces = Game.pieces();

        $scope.userPiece = pieces.user;
        $scope.statistics = Stats.getStats() || [];
        $scope.spaceNumbers = [0,1,2,3,4,5,6,7,8];

        /*
         * Triggered when it's the AI's turn to move
         *
         * The aiTurn variable calls the service to take the turn.
         * This variable returns an object which tells the controller what to display.
         */
        function aiMoves(){
            // returns space to mark, winner if at all, and if finished
            var aiTurn = Game.aiTurn();

            if(aiTurn.space > -1) {
                $scope['space' + aiTurn.space] = pieces.ai;
            }

            if(aiTurn.hasWon) {
                $scope.winner = 'ai';
                Stats.addStats({ winner: 'ai', moves: Game.getMoves() });
                updateStats();
            } else if(aiTurn.finished || aiTurn.space === -1){
                $scope.winner = 'tie';
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
         *
         * Clears grid and resets variables in service, then resets the pieces so that X is first determines if AI is first
         */
        $scope.resetGame = function(){
            clearGrid();
            Game.newGame();
            pieces = Game.pieces();
            $scope.userPiece = pieces.user;

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
                $scope['space' + space] = pieces.user;
                Game.addMove('u', space);
                if(Game.checkMove(space)){
                    $scope.winner = 'user';
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
         * @param {Number} which Which game was selected to replay
         */
        $scope.replay = function(which){
            var moves = angular.copy($scope.statistics[which].moves),
                move,
                x = true; // first move is always x

            clearGrid();

            $scope.userPiece = '';

            // cancel any in-progress playbacks
            if($scope.counter){
                $interval.cancel($scope.counter);
            }

            // emulate a real game with a 1s timeout and place pieces on the grid
            $scope.counter = $interval(function(){
                if(moves.length){
                    move = moves.shift();
                    $scope['space' + move[1]] = x ? 'X' : 'O';
                    x = !x;
                } else {
                    $interval.cancel($scope.counter);
                    $scope.winner = $scope.statistics[which].winner;
                }
            }, 1000);
        }
    }]);












