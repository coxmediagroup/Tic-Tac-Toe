'use strict';

angular.module('app').service('WinnerService', function ($http, $q) {
    var winnerService = this;
	
	var theWinningCombination = new Array(3);
	
	//squares is an array of 9 characters
	//each character is either an 'X', 'O', or ''
	winnerService.winningCombination = function(squares) {
		var deffered = $q.defer();
		$http.get('/winner/winningCombination/' + squares.toString()).success(function (data) {
			var splitData = data.split(",");
			var winningCombinationIntArray = new Array(splitData[0], splitData[1], splitData[2]);
			theWinningCombination = winningCombinationIntArray;
			deffered.resolve();
	    })
		
		return deffered.promise;
	}
	
	winnerService.theWinningCombination = function() { return theWinningCombination; }
	
});