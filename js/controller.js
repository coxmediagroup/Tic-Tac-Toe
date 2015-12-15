/* controller.js */
angular.module("ticTacToeApp").controller("gameCtrl", function($scope){
	$scope.turn = 1;
	$scope.gameState = [
						'','','',
						'','','',
						'','','',
						];
	$scope.userClick = function(index){
		if($scope.gameState[index] === ""){
			// this logic needs to be moved into a service...
			if($scope.turn === 1){
				$scope.gameState[index] = "x";
				if(index === 4){
					$scope.gameState[0] = "o";
				} else {
					$scope.gameState[4] = "o";					
				}
				$scope.turn = $scope.turn + 2;
			}
		}
	}
});