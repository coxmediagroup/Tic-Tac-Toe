var mainModule = angular.module('tictactoeApp', ['ui.bootstrap']);

var gameCtrl = mainModule.controller('GameCtrl', function ($scope, $modal, aiFactory) {
    $scope.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    $scope.turn = 1 //Start on the player's turn

    $scope.getButtonClass = function ( index ) {
        playerClasses = { 0: "btn-default", 1: "btn-computer", 2: "btn-player" };
        var btnClass = playerClasses [ $scope.grid [ index ] ];
        
        if (( index % 3 ) == 0 ) {
            btnClass += " clear-left";
        }
        return btnClass;
    }
  
    $scope.clickButton = function ( index ) {
        $scope.grid [ index ] = 2;
        var nextMove = aiFactory.calculateMove ( $scope.grid.slice( 0 ) );
        if ( nextMove != undefined ) {
            $scope.grid [ nextMove ] = 1;
        }
        var gameStatus = aiFactory.getGameStatus ( $scope.grid.slice( 0 ) );
        if ( gameStatus.status > 0 ) {
            var statusMessage = { 1: "It is a tie!", 2: "The computer has won!", 3: "You have won!" };
            $scope.endOfGame( statusMessage [ gameStatus.status ] );
        }
    }

    $scope.endOfGame = function (status) {
        //Modal dialog that pops up when the game ends
        var modalInstance = $modal.open({
            templateUrl: 'modal-gameend.html',
            controller: function ($scope, $modalInstance, status) {
                $scope.status = status;
                $scope.ok = function () {
                    $modalInstance.close();
                };
            },
            windowClass: 'modal-gameend',
            backdrop: false,
            keyboard: false,
            resolve: {
                status: function () {
                    return status;
                }
            }
        });
    
        modalInstance.result.then(function () {
            if ( $scope.turn == 0 ) {
                $scope.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0];
                $scope.turn = 1;
            } else {
                $scope.grid = [0, 0, 0, 0, 1, 0, 0, 0, 0];
                $scope.turn = 0;
            }
        });
    };


});

