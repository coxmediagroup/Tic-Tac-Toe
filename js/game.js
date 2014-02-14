var mainModule = angular.module('tictactoeApp', []);

var gameCtrl = mainModule.controller('GameCtrl', function ($scope) {
  $scope.test = 'X';
});

gameCtrl.directive('gameButton', function() {
    return {
      restrict: 'E',
      templateUrl: 'gamebtn.html'
    };
 });