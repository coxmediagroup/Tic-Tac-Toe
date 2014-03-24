'use strict';
/**
 * Reference: http://ostermiller.org/tictactoeexpert.html, http://www.cs.berkeley.edu/~bh/pdf/v1ch06.pdf, http://en.wikipedia.org/wiki/Tic-tac-toe, http://www.genetic-programming.org/sp2003/Hochmuth.pdf
 */

/**
 * Tic Tac Toe Game Controller
 *
 * @param $scope
 * @param $rootScope
 * @param $location
 * @param $http
 * @param $timeout
 * @constructor
 */
function AppCtrl($scope, $rootScope, $location, $http, $timeout) {
    var matrixSize = 3, empty = 0, player = 1, robot = 2, displayMsgFor = 4000;

    /**
     * Start a new game
     */
    $scope.startGame = function () {
        $scope.hasWinner = false;
        $scope.moves = new Array();
        $scope.rows = new Array();
        for(var i = 0 ; i < matrixSize; i++) {
            var cols = [0,0,0];
            $scope.rows.push(cols);
        }

        // Let computer start first
        $scope.robotPlay();
    }

    /**
     * Display an alert
     *
     * @param msg
     */
    $scope.showMessage = function(msg){
        $scope.message = msg;
        $scope.displayMessage = true;
        $timeout(function(){
            $scope.displayMessage = false;
        }, displayMsgFor)
    }

    /**
     * User play handler
     *
     * @param event
     * @param index
     * @param parentIndex
     */
    $scope.userPlay = function(event, index, parentIndex) {
        if($scope.hasWinner) {
            $scope.showMessage ('Game has a winner.');
            return;
        }
        $scope.moves.push('You Played ' + index.toString() + "," + parentIndex.toString());
        if($scope.rows[parentIndex][index] == empty) {
            $scope.rows[parentIndex][index] = player;
            $scope.checkWinner(player); //check if the player won
            if($scope.hasWinner) {
                var msg = 'Congrats you won';
                $scope.moves.push(msg); $scope.showMessage(msg);
                return;
            }
            $scope.robotPlay();
            $scope.checkWinner(robot);  //check if robot won
            if($scope.hasWinner) {
                var msg = 'Sorry I won';
                $scope.moves.push(msg); $scope.showMessage(msg);
                return;
            }
        } else {
            $scope.showMessage('Oops! that cell is already taken');
        }
    }

    /**
     * Computer play handler
     */
    $scope.robotPlay = function() {

        //try to win
        //by row
        var playRow = $scope.checkRows(matrixSize - 1, robot);
        if(playRow > -1) {
            if($scope.playRow(playRow)) return;
        }

        //by column
        var playColumn = $scope.checkColumns(matrixSize - 1, robot);
        //check if the user is going to complete a column
        if(playColumn > -1) {
            if($scope.playColumn(playColumn)) return;
        }

        //by cross
        var blockCross = $scope.checkCross(matrixSize - 1, robot);
        if(blockCross > -1) {
            if($scope.playCross(blockCross)) return;
        }

        //if winning does not work then block user from winning
        playRow = $scope.checkRows(matrixSize - 1, player);
        if(playRow > -1) {
            if($scope.playRow(playRow)) return;
        }

        playColumn = $scope.checkColumns(matrixSize - 1, player);
        if(playColumn > -1) {
            if($scope.playColumn(playColumn)) return;
        }

        blockCross = $scope.checkCross(matrixSize - 1, player);
        if(blockCross > -1) {
            if($scope.playCross(blockCross)) return;
        }

        // otherwise robot has preferred positions
        for(var i = 0; i < $scope.preferredPositions.length; i++) {
            if($scope.rows[$scope.preferredPositions[i][0]][$scope.preferredPositions[i][1]] == empty){
                $scope.rows[$scope.preferredPositions[i][0]][$scope.preferredPositions[i][1]] = robot;
                $scope.moves.push('I Played ' + $scope.preferredPositions[i][0].toString() + "," + $scope.preferredPositions[i][1].toString());
                return;
            }
        }
        $scope.showMessage('A draw!');
    }

    /**
     * Check rows to see who has what populated
     *
     * @param checkLimit
     * @param checkfor
     * @returns {number}
     */
    $scope.checkRows = function(checkLimit, checkfor) {
        var positionsFull = 0;
        for(var i = 0; i < matrixSize; i++) {
            var positionsFull = 0;
            for(var j = 0; j < matrixSize; j++) {
                if($scope.rows[i][j] == checkfor) {
                    positionsFull++;
                }
            }
            if(checkLimit == positionsFull) return i;
        }
        return -1;
    }

    /**
     * Check columns to see who has what populated
     *
     * @param checkLimit
     * @param checkfor
     * @returns {number}
     */
    $scope.checkColumns = function(checkLimit, checkfor) {
        var positionsFull = 0;
        for(var j = 0; j < matrixSize; j++) {
            var positionsFull = 0;
            for(var i = 0; i < matrixSize; i++) {
                if($scope.rows[i][j] == checkfor) {
                    positionsFull++;
                }
            }
            if(checkLimit == positionsFull) return j;
        }
        return -1;
    }


    /**
     * Determine if player has a cross
     *
     * @param checkLimit
     * @param checkfor
     * @returns {number}
     */
    $scope.checkCross = function(checkLimit, checkfor) {
        var positionsFull = 0;
        var i = 0;
        for(var j = 0; j < matrixSize; j++) {
            if($scope.rows[i][j] == checkfor) {
                positionsFull++;
            }
            if(checkLimit == positionsFull) return 1;
            i++;
        }

        //check for the second cross line
        positionsFull = 0;
        i = 2;
        for(var j = 0; j < matrixSize; j++) {
            if($scope.rows[i][j] == checkfor) {
                positionsFull++;
            }
            if(checkLimit == positionsFull) return 2;
            i--;
        }
        return -1;
    }

    /**
     * Determine winner
     *
     * @param checkfor
     */
    $scope.checkWinner = function(checkfor){
        var i=0, j =0;
        //check if there is a winning row

        $scope.hasWinner = $scope.checkRows(matrixSize, checkfor) > -1;
        if($scope.hasWinner) { return; }

        $scope.hasWinner = $scope.checkColumns(matrixSize, checkfor) > -1;
        if($scope.hasWinner) { return; }

        $scope.hasWinner = $scope.checkCross(matrixSize, checkfor) > -1;
        if($scope.hasWinner) { return; }

    }

    /**
     * Makes a play in a row for computer
     *
     * @param rowNo
     * @returns {boolean}
     */
    $scope.playRow = function(rowNo) {
        for(var i = 0; i < matrixSize; i++) {
            if($scope.rows[rowNo][i] == empty) {
                $scope.rows[rowNo][i] = robot;
                $scope.moves.push('I Played ' + rowNo.toString() + "," + i.toString());
                return true;
            }
        }
        return false;
    }

    /**
     * Makes a play in a column for computer
     *
     * @param columnNo
     * @returns {boolean}
     */
    $scope.playColumn = function(columnNo) {
        for(var i = 0; i < matrixSize; i++) {
            if($scope.rows[i][columnNo] == empty) {
                $scope.rows[i][columnNo] = robot;
                $scope.moves.push('I Played ' + i.toString() + "," + columnNo.toString());
                return true;
            }
        }
        return false;
    }

    /**
     * Makes a play in a cross for the computer
     *
     * @param crossNo
     * @returns {boolean}
     */
    $scope.playCross = function(crossNo) {
        var i = crossNo == 1 ? 0 : matrixSize - 1;
        for(var j = 0; j < matrixSize; j++) {
            if($scope.rows[i][j] == empty) {
                $scope.rows[i][j] = robot;
                $scope.moves.push('I Played ' + i.toString() + "," + j.toString());
                return true;
            }
            if(crossNo == 1) i++;
            else i--;
        }
        return false;
    }


    // Preferred positions for computer player
    $scope.preferredPositions = new Array();
    $scope.preferredPositions.push([1,1]);
    $scope.preferredPositions.push([0,1]);
    $scope.preferredPositions.push([1,0]);
    $scope.preferredPositions.push([2,1]);
    $scope.preferredPositions.push([1,2]);
    $scope.preferredPositions.push([0,0]);
    $scope.preferredPositions.push([0,2]);
    $scope.preferredPositions.push([2,2]);

    //start the game
    $scope.startGame();





}