'use strict';

angular.module('tictactoe')
    .controller('GameCtrl', ['$scope', 'Stats', 'Game', function($scope, Stats, Game){
        var player = Game.player();

        $scope.spaceNumbers = [1,2,3,4,5,6,7,8,9];

        $scope.spaceClicked = function(which){
            $scope['space' + which] = 'X';
            Game.playerMoved(which);
        }
    }]);