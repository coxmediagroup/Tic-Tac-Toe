'use strict';

/* Controllers */

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

}