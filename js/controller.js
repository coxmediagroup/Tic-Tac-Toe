/* controller.js */
angular.module("ticTacToeApp").controller("gameCtrl", function($scope, $timeout, ai){
	$scope.won = false;
	$scope.tie = false;
	$scope.gameState = [
						'','','',
						'','','',
						'','','',
						];
	$scope.turn = 1;
	$scope.resetGame = function(){
		$scope.gameState = [
						'','','',
						'','','',
						'','','',
						];
		$scope.won = false;
		$scope.tie = false;
		$scope.turn = 1;
		ai.reset();
	};

	$scope.$watchCollection("gameState", function(newState, oldState){
		$scope.turn = ai.turn($scope.gameState);
		$scope.won = ai.hasWon();
		$scope.tie = ai.hasTied();
	});

	$scope.userClick = function(index){
		if($scope.gameState[index] === "" && !$scope.won && !$scope.tie){
			$scope.gameState[index] = "x";
			var nextPosition = ai.nextPlay($scope.gameState);
			$scope.gameState[nextPosition] = "o";
		}
	}
	
	$timeout(function() {
		$(".hide-during-load").removeClass("hide-during-load");
		$scope.loaded = true;
	}, 1000);
	
});