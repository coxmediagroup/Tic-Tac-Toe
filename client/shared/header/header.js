'use strict';

angular.module('tictactoe')
    .controller('HeaderCtrl', ['$scope', function($scope){
        $scope.navlinks = [
            {
                'title': 'Play',
                'link': 'play'
            },
            {
                'title': 'Replay',
                'link': 'replay'
            },
            {
                'title': 'Statistics',
                'link': 'statistics'
            }
        ];
    }]);