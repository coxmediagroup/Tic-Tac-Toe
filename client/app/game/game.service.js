'use strict';

/*
 * Returns game logic to keep from complicating controller
 */
angular.module('tictactoe')
    .factory('Game', function(){
        var module,
            playerFirst = true,
            playerTurn = true,
            playerMatrix = [0,0,0,0,0,0,0,0,0],
            aiMatrix = [0,0,0,0,0,0,0,0,0];

        /*
         * Grid is numbered this way:
         *
         *   1, 2, 3
         *   4, 5, 6
         *   7, 8, 9
         *
         * The binary equivalent of the 8 winning strategies are in 'winningStrategies' (eg. 1,8,64 = 73)
         * The priority for randomly choosing the space in in 'spacePriority'
         */
        var winningStrategies = [7, 56, 73, 84, 146, 273, 292, 448];
        var spacePriority = '101020101';

        function checkForWin(matrix){
            var c;

            // convert positions to their binary equivalent
            var binaryMatrix = parseInt(matrix.join(''), 2);

            console.log(binaryMatrix);

            // go through the winning strategies to find a possible match
            for(c = 0; c < winningStrategies.length; c++){
                if((winningStrategies[c] & binaryMatrix) === winningStrategies[c]){
                    alert('Player Wins!');
                }
            }
        }

        function playerMoved(space){
            playerMatrix[space - 1] = 1;
            checkForWin(playerMatrix);
        }

        // 1<<0 through 1<<8


        function player(){
            return playerFirst ? 'X' : 'O';
        }

        module = {
            player: player,
            playerMoved: playerMoved
        };

        return module;
    });