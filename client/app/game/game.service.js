'use strict';

/*
 * Service container for game logic to keep from complicating controller
 */
angular.module('tictactoe')
    .factory('Game', ['Stats', function(Stats){
        var module,
            userFirst = true,
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

        function checkForWin(player){
            var c,
                matrix = player === 'player' ? userMatrix : aiMatrix;

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
            userMatrix[space] = 1;
            usersTurn = false;
            return checkForWin('player');
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

        // function to start AI logic
        // function returns the space taken and if the AI won
        function aiTurn(){
            var space = -1,
                hasWon,
                freeSpaces = [],
                blockMove = [],
                userBinary = parseInt(userMatrix.join(''), 2),
                aiBinary = parseInt(aiMatrix.join(''), 2),
                c,
                strategy,
                toMove = [];

            // check free spaces
            for(c = 0; c < userMatrix.length; c++){
                if(!userMatrix[c] && !aiMatrix[c]){
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

            function checkStrategies(player, leftToComplete, cb, t){
                var c, b,
                    left,
                    diff,
                    playerBinary = player === 'ai' ? aiBinary : userBinary;

                if(space === -1) {

                    console.log(t);

                    for (c = 0; c < winningStrategies.length; c++) {
                        strategy = winningStrategies[c];

                        diff = strategy - (strategy & playerBinary);

                        left = diff.toString(2).match(/1/g).length;

                        // if there is one left to complete row, immediately pick
                        if (left === leftToComplete) {
                            for (b = 0; b < 9; b++) {
                                if ((diff & (1 << b)) === (1 << b)) {
                                    if (freeSpaces.indexOf(8 - b) > -1) {
                                        console.log(cb);
                                        cb(8 - b);
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // check for immediate win
            checkStrategies('ai', 1, function(val){ space = val; },'aa');

            // block player from win
            checkStrategies('player', 1, function(val){ space = val; },'bb');

            // check single case that the following code doesn't solve, the diagonal corner issue
            if(space === -1){
                if(userBinary === 68 || userBinary === 257){
                    for(c = 0; c < freeSpaces.length; c++){
                        if(spacePriority[freeSpaces[c]] === '0'){
                            toMove.push(freeSpaces[c]);
                        }
                    }

                    if(toMove.length){
                        console.log('special case');
                        space = pickRandom(toMove);
                    }
                }
            }

            checkStrategies('player', 2, function(val){ blockMove.push(val); },'cc');

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
                    space = pickRandom(toMove);
                }
            }

            checkStrategies('ai', 2, function(val){ space = val; },'dd');

            // check single case that the following code doesn't solve, the diagonal corner issue
            if(space === -1){
                if(userBinary === 68 || userBinary === 257){
                    for(c = 0; c < freeSpaces.length; c++){
                        if(spacePriority[freeSpaces[c]] === '0'){
                            toMove.push(freeSpaces[c]);
                        }
                    }

                    if(toMove.length){
                        console.log('special case');
                        space = pickRandom(toMove);
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
                    space = pickRandom(toMove);
                }
            }

            // mark the matrix
            if(space !== -1){
                aiMatrix[space] = 1;
                addMove('ai', space);
            }

            // set hasWon
            hasWon = checkForWin('ai');

            usersTurn = true;

            return {
                space: space,
                hasWon: hasWon
            }
        }

        function addMove(player, space){
            var shortenedPlayer = player === 'ai' ? 'a' : 'u';
            moveMatrix.push(shortenedPlayer + space);
        }

        function pickRandom(arr){
            return arr[Math.floor(Math.random() * arr.length)];
        }

        function pieces(){
            if(userFirst){
                return { player: 'X', ai: 'O' }
            } else {
                return { player: 'O', ai: 'X' }
            }
        }

        function newGame(){
            userFirst = true;
            usersTurn = true;
            userMatrix = [0,0,0,0,0,0,0,0,0];
            aiMatrix = [0,0,0,0,0,0,0,0,0];
            winner = null;
            moveMatrix = [];
        }

        function getMoves(){
            return moveMatrix;
        }

        // return only the functions that are used by the controller
        module = {
            checkMove: checkMove,
            canMove: canMove,
            aiTurn: aiTurn,
            pieces: pieces,
            newGame: newGame,
            addMove: addMove,
            getMoves: getMoves
        };

        return module;
    }]);