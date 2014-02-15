var mainModule = angular.module('tictactoeApp', []);

var gameCtrl = mainModule.controller('GameCtrl', function ($scope) {
  $scope.grid = ["0","1","2","3","4","5","6","7","8"];
  
  $scope.getButtonText = function(index){
      return index;
  }
  
  $scope.getButtonClass = function(index){
      if((index%3)==0){
          return "clear-left";
      } else{
          return "";
      }
  }
});

