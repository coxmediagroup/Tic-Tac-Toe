'use strict';

/*
 * Service container for game logic to keep from complicating controller
 * The factory service is used similar to a revealing module pattern
 */
angular.module('tictactoe')
    .factory('Game', ['Stats', function(Stats){
        var userFirst = true,
            usersTurn = true,
            userMatrix = [0,0,0,0,0,0,0,0,0],
            aiMatrix = [0,0,0,0,0,0,0,0,0],
            winner = null,
            moveMatrix = [];

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

        /*
         * Returns true if player won
         */
        function checkForWin(player){
            var c,
                matrix = player === 'user' ? userMatrix : aiMatrix;

            // convert positions to their binary equivalent
            var binaryMatrix = parseInt(matrix.join(''), 2);

            // go through the winning strategies to find a possible match, which uses the bitwise AND operator:
            // if the user pieces binary config matches exactly the winning strategy binary config, then true
            for(c = 0; c < winningStrategies.length; c++){
                if((winningStrategies[c] & binaryMatrix) === winningStrategies[c]){
                    winner = player;
                    return true;
                }
            }

            return false;
        }

        // checks the user move for win and sets variables
        // if there is a win, true is returned
        function checkMove(space){
            userMatrix[space] = 1;
            usersTurn = false;
            return checkForWin('user');
        }

        // returns winner string or null
        function gameOver(){
            return winner;
        }

        // returns true if space is occupied
        function spaceFree(space){
            return !userMatrix[space] && !aiMatrix[space];
        }

        // returns true if players turn
        function isPlayersTurn(){
            return usersTurn;
        }

        // returns true if the player can move
        function canMove(space){
            return isPlayersTurn() && spaceFree(space) && !gameOver();
        }

        /*
         * AI logic
         *
         * AI flow to choose a space:
         *
         * 1. compile list of open spaces
         * 2. check for immediate win and choose space
         * 3. check for immediate block of opponent to prevent win
         * 4. check for the opposite corner win
         * 5. make a list to possibly blocks
         * 6. if possible blocking exists, choose one based on priority and random choice
         * 7. choose a space to continue a strategy
         * 8. choose a space based on randomization, with more change given to higher priority spaces
         */
        function aiTurn(){
            var space = -1,
                hasWon,
                freeSpaces = [],
                blockMove = [],
                userBinary = parseInt(userMatrix.join(''), 2),
                aiBinary = parseInt(aiMatrix.join(''), 2),
                c, cc,
                strategy,
                toMove = [],
                finished,
                times;

            /*
             * Helper function to compare players pieces to the winning strategies
             */
            function checkStrategies(player, leftToComplete, cb){
                var c, b,
                    left,
                    diff,
                    playerBinary = player === 'ai' ? aiBinary : userBinary;

                if(space === -1) {
                    for (c = 0; c < winningStrategies.length; c++) {
                        strategy = winningStrategies[c];

                        diff = strategy - (strategy & playerBinary);

                        left = diff.toString(2).match(/1/g).length;

                        // if there is one left to complete row, immediately pick
                        if (left === leftToComplete) {
                            for (b = 0; b < 9; b++) {
                                if ((diff & (1 << b)) === (1 << b)) {
                                    if (freeSpaces.indexOf(8 - b) > -1) {
                                        cb(8 - b);
                                    }
                                }
                            }
                        }
                    }
                }
            }

            /*
             * Helper function to pick a random value from the array provided
             */
            function pickRandom(arr){
                return arr[Math.floor(Math.random() * arr.length)];
            }

            // 1. compile list of free spaces
            for(c = 0; c < userMatrix.length; c++){
                if(!userMatrix[c] && !aiMatrix[c]){
                    freeSpaces.push(c);
                }
            }
            // set finished to true if nothing left to do
            finished = freeSpaces.length === 1;

            // 2. check for immediate win
            checkStrategies('ai', 1, function(val){ space = val; });

            // 3. block player from immediate win
            checkStrategies('player', 1, function(val){ space = val; });

            // 4. check single case that the following code doesn't solve, the opposite diagonal corner win
            //    with this configuration, the opponent may win if the corner is selected, so select a side instead
            if(space === -1){
                if(userBinary === 68 || userBinary === 257){
                    for(c = 0; c < freeSpaces.length; c++){
                        if(spacePriority[freeSpaces[c]] === '0'){
                            toMove.push(freeSpaces[c]);
                        }
                    }

                    if(toMove.length){
                        space = pickRandom(toMove);
                    }
                }
            }

            // 5. find all possible ways the opponent may win
            checkStrategies('player', 2, function(val){ blockMove.push(val); });

            // 6. choose a blocking strategy
            if(space === -1 && blockMove.length) {
                for (c = 0; c < blockMove.length; c++) {
                    // priority 2 (center) is immediately picked
                    if (spacePriority[blockMove[c]] === '2') {
                        space = blockMove[c];
                    // priority 1 (corners) is second most important
                    } else if (spacePriority[blockMove[c]] === '1') {
                        toMove.push(blockMove[c]);
                    }
                }

                // if all priority 1, choose a random one
                if (space === -1 && toMove.length) {
                    space = pickRandom(toMove);
                }
            }

            // 7. choose a space to continue building on a strategy
            checkStrategies('ai', 2, function(val){ space = val; });

            // 8. pick one based on randomization with more chance given to the higher priority spaces
            if(space === -1) {
                for(c = 0; c < freeSpaces.length; c++){
                    // priorities are 0,1,2, which translates to 1,2,4
                    times = 1 << +spacePriority[freeSpaces[c]];
                    for(cc = 0; cc < times; cc++){
                        toMove.push(freeSpaces[c]);
                    }
                }

                if(toMove.length){
                    space = pickRandom(toMove);
                }
            }

            // mark the matrix and add move to game
            if(space !== -1){
                aiMatrix[space] = 1;
                addMove('a', space);
            }

            hasWon = checkForWin('ai');

            usersTurn = true;

            // return object to the controller
            return {
                space: space,
                hasWon: hasWon,
                finished: finished
            }
        }

        /*
         * Adds the move to the game
         */
        function addMove(player, space){
            moveMatrix.push(player + space);
        }

        /*
         * Returns the pieces based on who is first
         */
        function pieces(){
            if(userFirst){
                return { user: 'X', ai: 'O' }
            } else {
                return { user: 'O', ai: 'X' }
            }
        }

        /*
         * Reset the game
         */
        function newGame(){
            userFirst = !userFirst;
            usersTurn = userFirst;
            userMatrix = [0,0,0,0,0,0,0,0,0];
            aiMatrix = [0,0,0,0,0,0,0,0,0];
            winner = null;
            moveMatrix = [];
        }

        /*
         * Getter for the userFirst variable
         */
        function getUserFirst(){
            return userFirst;
        }

        /*
         * Getter for the moves
         */
        function getMoves(){
            return moveMatrix;
        }

        /*
         * Object returned for interaction with the conroller
         */
        return {
            checkMove: checkMove,
            canMove: canMove,
            aiTurn: aiTurn,
            pieces: pieces,
            newGame: newGame,
            addMove: addMove,
            getMoves: getMoves,
            getUserFirst: getUserFirst
        };
    }]);