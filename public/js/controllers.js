'use strict';

/* Controllers */

function AppCtrl($scope, $rootScope, $location, $http, $timeout) {
    var matrixSize = 3, empty = 0, player = 1, robot = 2, displayMsgFor = 4000;

    /**
     * Start new game
     */
    $scope.startGame = function () {
        $scope.hasWinner = false;
        $scope.moves = new Array();
        $scope.rows = new Array();
        for(var i = 0 ; i < matrixSize; i++) {
            var cols = [0,0,0];
            $scope.rows.push(cols);
        }
    }


}