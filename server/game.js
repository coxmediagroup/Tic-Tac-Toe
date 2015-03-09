
module.exports = (function() {
	/*
	 0 1 2
	 3 4 5
	 6 7 8
	*/
	var board = [
		undefined, undefined, undefined,
		undefined, undefined, undefined,
		undefined, undefined, undefined,
	];

	function canMove(tile) {
		return board[tile] === undefined;
	}
	
	/*
	 horizontal
	 0 == 1 == 2
	 3 == 4 == 5
	 6 == 7 == 8

	 vertical
	 0 == 3 == 6
	 1 == 4 == 7
	 2 == 5 == 8

	 diagonal
	 0 == 4 == 8
	 2 == 4 == 6
	*/
	return {
		hasWinner: function() {
			function checkHorizontal() {
				var b = board;
				return (b[0] != undefined && b[0] === b[1] && b[0] === b[2]) ||
					(b[3] != undefined && b[3] === b[4] && b[3] === b[5]) ||
					(b[6] != undefined && b[6] === b[7] && b[6] === b[8]);
			}
			function checkVertical() {
				var b = board;
				return (b[0] != undefined && b[0] === b[3] && b[0] === b[6]) ||
					(b[1] != undefined && b[1] === b[4] && b[1] === b[7]) ||
					(b[2] != undefined && b[2] === b[5] && b[2] === b[8]);
			}
			function checkAcross() {
				var b = board;
				return (b[0] != undefined && b[0] === b[4] && b[0] === b[8]) ||
					(b[2] != undefined && b[2] === b[4] && b[2] === b[6]);
			}
	
			return checkHorizontal() || checkVertical() || checkAcross();
		},
		hasMoves: function() {
			for (var i in board) {
				if (board[i] === undefined) {
					return true;
				}
			}
			return false;
		},
		selectTile: function(tile, player) {
			if (canMove(tile)) {
				board[tile] = player;
				return true;
			}
			return false;
		}
	};
}())
