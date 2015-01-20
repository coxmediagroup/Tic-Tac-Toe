'use strict';

angular.module('app').service('ComputerPlayerService', function ($http, $q) {
	
	var computerNextMoveIndex = -1;
	var errorMessage = "";
	
	//squares is an array of 9 characters
	//each character is either an 'X', 'O', or ''
	this.nextMove = function(squares) {
		var deffered = $q.defer();
		$http.get('/computerPlayer/nextMove/' + squares.toString()).success(function (data) {
			computerNextMoveIndex = parseInt(data);
			deffered.resolve();
	    })
	    .error(function () {
	    	errorMessage = "No squares left";
	    	deffered.resolve();
	    });
		
		return deffered.promise;
	}
	
	this.computerNextMoveIndex = function() { return computerNextMoveIndex; };
	
});