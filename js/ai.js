mainModule.factory('aiFactory', function() {
    
    var ai = {};
    
    //Array containing all combinations that would result in a win
    ai.combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];

    ai.getCombinations = function ( playerID, grid ) {
        /* This function will return an array containing the indices of the
           squares that, if filled, would give the given playerID 3 squares in
           a row */

        var returnList = [];
        
        //We first check if we already have any two in a row so that we can
        //complete the set
        for ( var i = 0; i < ai.combinations.length; i++ ){
            var combination = ai.combinations[i];
            
            var filledCount = 0;
            var notFilled = -1; //Holds which square hasn't yet been filled
            for ( var j = 0; j < combination.length; j++ ){
                if ( grid [ combination [ j ] ] == playerID ){
                    filledCount ++;
                } else {
                    notFilled = combination [ j ];
                }
            }
            
            if ( filledCount == 2 ){
                if ( grid [ notFilled ] === 0 ) {
                    returnList.push ( notFilled );
                }
            }
        }
        
        return returnList;
    }

    ai.calculateMove = function ( grid ) {
        /* This function will return the index of the square that would be the
        best next move for the computer to make */
        
        //If there are already 2 in a row then fill the last space
        var winningMoves = ai.getCombinations ( 1, grid );
        if ( winningMoves.length ) {
            return winningMoves [ 0 ];
        }

        //If the player has two in a row then block his last space
        var blockingMoves = ai.getCombinations ( 2, grid );
        if ( blockingMoves.length ) {
            return blockingMoves [ 0 ];
        }

        //Iterate through the open spaces, finding the moves that the player
        //will use to become winning combinations
        var playerNextMoves = [];
        for ( var i = 0; i < 9; i++ ){
            if ( grid [ i ] === 0 ) {
                
                //Clone our grid into a temporary grid for testing scenarios
                var tempGrid = grid.slice( 0 );
                tempGrid [ i ] = 2;
                var winningCombos = ai.getCombinations ( 2, tempGrid );
                
                if ( winningCombos.length == 2 ){
                    playerNextMoves.push(i);
                }
            }
        }

        //Iterate through the open spaces, finding the moves that will result in
        //the best possible winning combinations
        var bestMoveList = [[],[],[]];
        for ( var i = 0; i < 9; i++ ){
            if ( grid [ i ] === 0 ) {
                
                //Clone our grid into a temporary grid for testing scenarios
                var tempGrid = grid.slice( 0 );
                tempGrid [ i ] = 1;
                var winningCombos = ai.getCombinations ( 1, tempGrid );
                
                //If we have found a space that would give us two possible ways
                //to win
                if ( winningCombos.length == 2 ){
                    if ( playerNextMoves.indexOf( i ) != -1 ){
                        
                        //If filling the space would also block the player
                        //then definitely use this space
                        return i;
                    } else {
                        
                        //If it won't block the player put this move on the
                        //first level of our move list
                        bestMoveList [ 0 ].push( i );
                    }
                }

                //If we have found a space that would give us a possible way
                //to win
                if ( winningCombos.length == 1 ){
                    if ( playerNextMoves.indexOf( i ) != -1 ){
                        
                        //If filling the space would also block the player
                        //then add this to the second level of our move list
                        bestMoveList [ 1 ].push( i );
                    } else {
                        
                        //Otherwise put it on the last level of our move list
                        bestMoveList [ 2 ].push( i );
                    }
                }
            }
        }
        if ( bestMoveList [ 0 ].length ) {
            return bestMoveList [ 0 ][ 0 ];
        } else if ( bestMoveList [ 1 ].length ) {
            return bestMoveList [ 1 ][ 0 ];
        } else if ( bestMoveList [ 2 ].length ) {
            return bestMoveList [ 2 ][ 0 ];
        }
        
        //Play the center
        if ( grid [ 4 ] === 0 ) {
            return 4;
        }
        
        //Play an opposite corner to the player
        var cornerOpposites = { 0: 8, 8: 0, 2: 6, 6: 2};
        for ( var corner in cornerOpposites ) {
            if ( cornerOpposites.hasOwnProperty ( corner ) ) {   
                if ( grid [ corner ] == 2 ){
                    if ( grid [ cornerOpposites [ corner ] ] === 0 ){
                        return cornerOpposites [ corner ];
                    }
                }
            }
        }
        
        //Play any open corner, then any open side
        var playList = [ 0, 2, 6, 8, 1, 3, 5, 7 ];
        for ( var i = 0; i < playList.length; i++ ){
            if ( grid [ i ] === 0 ){
                return i;
            }
        }
    }
    
    ai.getGameStatus = function ( grid ) {
        /* This function will return a dictionary containing an integer
        representing the status of the game
        0 - No win
        1 - Tie
        2 - Computer wins
        3 - Player wins
        It will also return a winning combination if the computer of player won
        */

        //Check if the computer or player has 3 in a row on any combination
        for ( var i = 0; i < ai.combinations.length; i++ ){
            var combination = ai.combinations[i];
            
            var computerFilledCount = 0;
            var playerFilledCount = 0;
            for ( var j = 0; j < combination.length; j++ ){
                if ( grid [ combination [ j ] ] == 1 ){
                    computerFilledCount ++;
                }
                if ( grid [ combination [ j ] ] == 2 ){
                    playerFilledCount ++;
                }
            }
            
            if ( computerFilledCount == 3 ){
                
                //The computer has won
                return { status: 2, combination: combination };
            }
            
            if ( computerFilledCount == 3 ){
                
                //The player has won
                return { status: 3, combination: combination };
            }
        }
        
        //Iterate through all spaces, and if all are filled then there is
        //a tie
        var allFilled = true;
        for ( var i = 0; i < 9; i++ ){
            if ( grid [ i ] === 0 ) {
                allFilled = false;
            }
        }
        if ( allFilled == true ) {
            return { status: 1 };
        }
        
        return { status: 0 };
    }

    return ai;
});