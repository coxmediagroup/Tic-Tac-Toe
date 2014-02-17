var mainModule = angular.module('tictactoeApp', ['ui.bootstrap']);

var gameCtrl = mainModule.controller('GameCtrl', function ($scope, $modal, aiFactory, scoreFactory) {
    $scope.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    $scope.turn = 1 //Start on the player's turn

    $scope.getButtonClass = function ( index ) {
        
        //Used by the view to theme the square depending on which player
        //has filled it or whether it is unused.
        playerClasses = { 0: "btn-default", 1: "btn-computer", 2: "btn-player" };
        var btnClass = playerClasses [ $scope.grid [ index ] ];
        
        if (( index % 3 ) == 0 ) {
            btnClass += " clear-left";
        }
        return btnClass;
    }
  
    $scope.clickButton = function ( index ) {
        
        //When the player clicks a square, if it hasn't yet been filled, we
        //assign that square to the player and then determine the next move
        //of the computer. We then check whether the game has been completed.
        if ( $scope.grid [ index ] === 0 ){
            $scope.grid [ index ] = 2;
            var nextMove = aiFactory.calculateMove ( $scope.grid.slice( 0 ) );
            if ( nextMove != undefined ) {
                $scope.grid [ nextMove ] = 1;
            }
            var gameStatus = aiFactory.getGameStatus ( $scope.grid.slice( 0 ) );
            if ( gameStatus.status > -1 ) {
                var statusMessage = { 2: "It is a tie!", 1: "The computer has won!", 0: "You have won!" };
                scoreFactory.raiseScore( scoreFactory.playerIndex [ gameStatus.status ] );
                $scope.endOfGame( statusMessage [ gameStatus.status ] );
            }
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

