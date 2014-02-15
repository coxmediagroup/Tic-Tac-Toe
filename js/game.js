var mainModule = angular.module('tictactoeApp', []);

var gameCtrl = mainModule.controller('GameCtrl', function ($scope, aiFactory) {
    $scope.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0];

    $scope.getTurnText = function () {
        var turnText = { 0: "Computer's turn. Please wait...",
                         1: "Your turn. Click any open squre." }
        return turnText[$scope.turn];
    }

    $scope.getButtonText = function ( index ) {
        var playerSymbol = { 0 : "", 1 : "O", 2 : "X" };
        return playerSymbol [ $scope.grid [ index ] ];
    }
  
    $scope.getButtonClass = function ( index ) {
        if (( index % 3 ) == 0 ) {
            return "clear-left";
        } else{
            return "";
        }
    }
  
    $scope.clickButton = function ( index ) {
        $scope.grid [ index ] = 2;
        var nextMove = aiFactory.calculateMove( $scope.grid.slice( 0 ) );
        console.log( "Next move: " + nextMove );
        if ( nextMove != undefined ) {
            $scope.grid [ nextMove ] = 1;
        }
    }
  
});

