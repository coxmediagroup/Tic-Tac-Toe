var app = angular.module('ticTacToe', []);

 app.controller('mainController', function ($scope, $http, $window) {
 
 	var oMove = "O";
 	var xMove = "X";
 	var empty = "";

 	$scope.ticTacToeMoves =  []; //[[0,0],[0,2],[1,1],[2,2]];

 	// A Grid is simply a two dimensional array with a X and Y index position
 	// 3x3 grid:
 	$scope.gridVm = [[empty,empty,empty],[empty,empty,empty],[empty,empty,empty]];
 	// 4x4 grid:
	//$scope.gridVm = [[oMove,xMove,empty,empty],[empty, oMove,empty,empty],[xMove,empty,xMove,empty],[xMove,empty,empty,empty]];
 	
 	//applyTicTacToeMovesToGrid($scope.ticTacToeMoves,$scope.gridVm);

	function applyTicTacToeMovesToGrid(moves, grid) {
		
		moves.forEach(function(move,index) {
			if(move.length != 2)
			{
				alert("Invalid move object.");
				console.log("This game only supports two dimensional (X, Y) grid values. Invalid object length.")
			} else
			{
				if(index % 2 == 0) 
				{
					grid[move[0]][move[1]] = xMove;
				}
				else 
				{
					grid[move[0]][move[1]] = oMove;
				}
			}

		});
	}

	$scope.makeTicTacToeMove = function(rowIndex,columnIndex)
	{
		$scope.ticTacToeMoves.push([rowIndex,columnIndex]);
		applyTicTacToeMovesToGrid($scope.ticTacToeMoves,$scope.gridVm);
		// todo: Get AI move from server
	}

 });