'use strict';

var app = angular.module('app', []);

app.factory('gameBoard', function(){
	return new GameBoard();
})