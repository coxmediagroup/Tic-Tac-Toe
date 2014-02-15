var mainModule = angular.module('tictactoeApp', []);

var gameCtrl = mainModule.controller('GameCtrl', function ($scope) {
  $scope.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0];

  $scope.getButtonText = function(index){
      switch($scope.grid[index]){
          case 0:
              return "";
          case 1:
              return "O";
          case 2:
              return "X";
      }
  }
  
  $scope.getButtonClass = function(index){
      if((index%3)==0){
          return "clear-left";
      } else{
          return "";
      }
  }
  
  $scope.clickButton = function(index){
      $scope.grid[index] = 1;
  }
  
});

