/* directives.js */
angular.module("ticTacToeApp").directive("header", function(){
	return {
		restrict:'A',
		templateUrl:"header.html"
	}
});
angular.module("ticTacToeApp").directive("game", function(){
	return {
		restrict:'A',
		templateUrl:"game.html"
	}
});
angular.module("ticTacToeApp").directive("footer", function(){
	return {
		restrict:'A',
		templateUrl:"footer.html"
	}
});