'use strict';

/*
 * Service container for game logic to keep from complicating controller
 */
angular.module('tictactoe')
    .factory('Game', function(){
        var module,
            playerFirst = true,
            playerTurn = true,
            playerMatrix = [0,0,0,0,0,0,0,0,0],
            aiMatrix = [0,0,0,0,0,0,0,0,0],
            winner = null;

        /*
         * Grid is numbered this way:
         *
         *   1, 2, 3
         *   4, 5, 6
         *   7, 8, 9
         *
         * Grid has the following binary designation for bitwise operations
         *
         *   256 128 64
         *   32  16  8
         *   4   2   1
         *
         * The binary equivalent of the 8 winning strategies are in 'winningStrategies' (eg. 1,8,64 = 73)
         * The priority for randomly choosing the space in in 'spacePriority'
         */
        var winningStrategies = [7, 56, 73, 84, 146, 273, 292, 448];
        var spacePriority = '101020101';

        function checkForWin(player){
            var c,
                matrix = player === 'player' ? playerMatrix : aiMatrix;

            // convert positions to their binary equivalent
            var binaryMatrix = parseInt(matrix.join(''), 2);

            // go through the winning strategies to find a possible match
            for(c = 0; c < winningStrategies.length; c++){
                if((winningStrategies[c] & binaryMatrix) === winningStrategies[c]){
                    winner = player;
                    return true;
                }
            }

            return false;
        }

        function checkPlayer(space){
            playerMatrix[space - 1] = 1;
            return checkForWin(player);
        }

        // returns winner string or null
        function gameOver(){
            return winner;
        }

        // returns true if space is occupied
        function spaceTaken(space){
             return !playerMatrix[space] && !aiMatrix[space];
        }

        // returns true if players turn
        function playersTurn(){
            return;
        }

        // returns true if the player can move
        function canMove(space){
            return playersTurn() && !spaceTaken(space) && !gameOver();
        }

        // function to start AI logic
        // function returns the space taken and if the AI won
        function aiTurn(){
            var space,
                hasWon;

            // Steps:
            // 1. checks free spaces
            // 2. check to see if needs to block player
            // 3. check which space would complete a strategy
            // 4. choose based on priority


            return {
                space: space,
                hasWon: hasWon
            }
        }

        // 1<<0 through 1<<8


        function pieces(){
            if(playerFirst){
                return { player: 'X', ai: 'O' }
            } else {
                return { player: 'O', ai: 'X' }
            }
        }

        module = {
            player: player,
            checkPlayer: checkPlayer,
            canMove: canMove,
            aiTurn: aiTurn,
            pieces: pieces
        };

        return module;
    });