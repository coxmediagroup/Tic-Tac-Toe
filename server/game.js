
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
	
	function hasWinner() {
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
	}
	
	function hasMoves() {
		for (var i in board) {
			if (board[i] === undefined) {
				return true;
			}
		}
		return false;
	}
	
	function selectTile(tile, player) {
		if (canMove(tile)) {
			board[tile] = player;
		}
		var resp = {
			player: player,
			winner: hasWinner(),
			hasMovesLeft: hasMoves(),
			board: board
		}
		return resp;
	}

	function resetBoard() {
		for (var i in board) {
			board[i] = undefined;
		}
	}
	
	return {
		hasWinner: hasWinner,
		hasMoves: hasMoves,
		selectTile: selectTile,
		reset: resetBoard
	};
}())
