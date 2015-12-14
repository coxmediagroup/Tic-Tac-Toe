/* controller.js */
angular.module("ticTacToeApp").controller("gameCtrl", function($scope){
	$scope.turn = 1;
	$scope.gameState = [
						'','','',
						'','','',
						'','','',
						];
});