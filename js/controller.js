/* controller.js */
angular.module("ticTacToeApp").controller("gameCtrl", function($scope, ai){
	$scope.gameState = [
						'','','',
						'','','',
						'','','',
						];
	$scope.turn = 1;
	$scope.$watchCollection("gameState", function(newState, oldState){
		$scope.turn = ai.turn($scope.gameState);
	});
	$scope.userClick = function(index){
		if($scope.gameState[index] === ""){
			$scope.gameState[index] = "x";
			var nextPosition = ai.nextPlay($scope.gameState);
			$scope.gameState[nextPosition] = "o";
		}
	}
});