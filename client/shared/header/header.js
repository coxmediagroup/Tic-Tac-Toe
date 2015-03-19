'use strict';

angular.module('tictactoe')
    .controller('HeaderCtrl', ['$scope', function($scope){
        $scope.navlinks = [
            {
                'title': 'Play',
                'link': 'play'
            },
            {
                'title': 'Statistics',
                'link': 'statistics'
            },
            {
                'title': 'Instructions',
                'link': 'instructions'
            }
        ];
    }]);