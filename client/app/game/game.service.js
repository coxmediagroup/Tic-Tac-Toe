'use strict';

/*
 * Service container for game logic to keep from complicating controller
 */
angular.module('tictactoe')
    .factory('Game', ['Stats', function(Stats){
        var module,
            playerFirst = true,
            playersTurn = true,
            playerMatrix = [0,0,0,0,0,0,0,0,0],
            aiMatrix = [0,0,0,0,0,0,0,0,0],
            winner = null;

        /*
         * Grid is numbered this way:
         *
         *   0, 1, 2
         *   3, 4, 5
         *   6, 7, 8
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

        function checkMove(space){
            playerMatrix[space] = 1;
            playersTurn = false;
            return checkForWin('player');
        }

        // returns winner string or null
        function gameOver(){
            return winner;
        }

        // returns true if space is occupied
        function spaceFree(space){
             return !playerMatrix[space] && !aiMatrix[space];
        }

        // returns true if players turn
        function isPlayersTurn(){
            return playersTurn;
        }

        // returns true if the player can move
        function canMove(space){
            return isPlayersTurn() && spaceFree(space) && !gameOver();
        }

        // function to start AI logic
        // function returns the space taken and if the AI won
        function aiTurn(){
            var space = -1,
                hasWon,
                freeSpaces = [],
                blockMove = [],
                playerBinary = parseInt(playerMatrix.join(''), 2),
                aiBinary = parseInt(aiMatrix.join(''), 2),
                b,
                c,
                w,
                diff,
                left,
                toMove = [];

            // check free spaces
            for(c = 0; c < playerMatrix.length; c++){
                if(!playerMatrix[c] && !aiMatrix[c]){
                    freeSpaces.push(c);
                }
            }

            /*
             * AI flow to choose a space:
             *
             * 1. check for immediate win and choose space
             * 2. check for immediate block of opponent to prevent win
             * 3. make a list to possibly block
             * 4. if possible blocking exists, choose one based on priority and random choice
             * 5. choose a space to continue a strategy
             * 6. choose a space based on priority
             */

            // check for immediate win
            for(c = 0; c < winningStrategies.length; c++) {
                w = winningStrategies[c];

                diff = w - (w & aiBinary);

                left = diff.toString(2).match(/1/g).length;

                // if there is one left to complete row, immediately pick
                if (left === 1) {
                    for (b = 0; b < 9; b++) {
                        if ((diff & (1 << b)) === (1 << b)) {
                            if(freeSpaces.indexOf(8 - b) > -1) {
                                console.log('a');
                                space = 8 - b;
                            }
                        }
                    }
                }
            }

            // check single case that the following code doesn't solve, the diagonal corner issue
            if(space === -1){
                if(playerBinary === 68 || playerBinary === 257){
                    for(c = 0; c < freeSpaces.length; c++){
                        if(spacePriority[freeSpaces[c]] === '0'){
                            toMove.push(freeSpaces[c]);
                        }
                    }

                    if(toMove.length){
                        console.log('special case');
                        space = toMove[Math.floor(Math.random() * toMove.length)];
                    }
                }
            }

            // check to see if needs to block player
            if(space === -1) {
                for (c = 0; c < winningStrategies.length; c++) {
                    w = winningStrategies[c];

                    // use bitwise operation to compare difference between this strategy and players pieces
                    diff = w - (w & playerBinary);

                    // counts the unoccupied spaces in this strategy
                    left = diff.toString(2).match(/1/g).length;

                    // if there is one left to complete row, it needs to be immediately blocked
                    if (left === 1) {
                        for (b = 0; b < 9; b++) {
                            if ((diff & (1 << b)) === (1 << b)) {
                                console.log('b');
                                if(freeSpaces.indexOf(8 - b) > -1) {
                                    space = 8 - b;
                                }
                            }
                        }
                    }

                    // if there are two left to complete row, add to list to possibly block
                    if (space === -1 && left === 2) {
                        for (b = 0; b < 9; b++) {
                            if ((diff & (1 << b)) === (1 << b)){
                                if(freeSpaces.indexOf(8 - b) > -1) {
                                    blockMove.push(8 - b);
                                }
                            }
                        }
                    }
                }
            }

            // choose a blocking strategy
            if(space === -1 && blockMove.length) {
                for (c = 0; c < blockMove.length; c++) {
                    // priority 2 is immediately picked
                    if (spacePriority[blockMove[c]] === '2') {
                        console.log('c');
                        space = blockMove[c];
                    // priority 1 is second most important
                    } else if (spacePriority[blockMove[c]] === '1') {
                        toMove.push(blockMove[c]);
                    }
                }

                // if all priority 1, choose a random one
                if (space === -1 && toMove.length) {
                    console.log('d');
                    space = toMove[Math.floor(Math.random() * toMove.length)];
                }
            }

            // choose a strategy when there are no other priorities and at least one piece
            if(space === -1){
                for(c = 0; c < winningStrategies.length; c++) {
                    w = winningStrategies[c];

                    diff = w - (w & aiBinary);

                    left = diff.toString(2).match(/1/g).length;

                    // if there is one left to complete row, immediately pick
                    if (left === 2) {
                        for (b = 0; b < 9; b++) {
                            if ((diff & (1 << b)) === (1 << b)) {
                                if(freeSpaces.indexOf(8 - b) > -1) {
                                    console.log('e');
                                    space = 8 - b;
                                }
                            }
                        }
                    }
                }
            }

            // just pick based on priority
            if(space === -1) {
                for (c = 0; c < freeSpaces.length; c++) {
                    // priority 2 is immediately picked
                    if (spacePriority[freeSpaces[c]] === '2') {
                        console.log('f');
                        space = freeSpaces[c];
                        // priority 1 is second most important
                    } else if (spacePriority[freeSpaces[c]] === '1') {
                        toMove.push(freeSpaces[c]);
                    }
                }

                if (space === -1 && toMove.length) {
                    console.log('g');
                    space = toMove[Math.floor(Math.random() * toMove.length)];
                }
            }

            // mark the matrix
            aiMatrix[space] = 1;

            // set hasWon
            hasWon = checkForWin('ai');

            playersTurn = true;

            return {
                space: space,
                hasWon: hasWon
            }
        }

        function pieces(){
            if(playerFirst){
                return { player: 'X', ai: 'O' }
            } else {
                return { player: 'O', ai: 'X' }
            }
        }

        module = {
            checkMove: checkMove,
            canMove: canMove,
            aiTurn: aiTurn,
            pieces: pieces
        };

        return module;
    }]);