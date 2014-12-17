angular.module('tictactoeApp', [])
.config(function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})
.controller('TicTacToeController', ['$scope', '$http', function($scope, $http){
	$scope.newGame = function() {
		$http.get('http://localhost:8000/api/game/new').success(function(data, status, headers, config) {
		  	if(data.status=="success") {
		  		$scope.serverGame = data.game;
		  	}
		  }).error(function(data, status, headers, config) {
		  	alert(data.message);
		  });
	};

	$scope.makeMove = function(position) {
		var url = 'http://localhost:8000/api/game/' + $scope.serverGame.gameId + '/makeMove/'
		$http.post(url, {player:'X', position:position})
		  .success(function(data, status, headers, config) {
		  	if(data.status=="success") {
		  		$scope.serverGame = data.game;
		  	}
		  })
		  .error(function(data, status, headers, config) {
		  	alert(data.message);
		  });
	};
 }]);

