/* This file is for anything and everything dealing with actual game play */

function determineIfWin() {
	//Right, so the below logic isn't enitrely awesome.
	//Should improve on it at some point
	
	/* The "each" stuff essentially is checking if there are any
	 * matches horizontally while also building up a list to check
	 * for other directional matches later */
	var gameboard = [];
	var isWinner = false;
	//Don't initialize a variable each time through the loop! Go through and fix!
	$("#board tr").each(function() {
		var rowData = $(this).find('td');
		var firstCell = rowData.eq(0).text();
		var secondCell = rowData.eq(1).text();
		var thirdCell = rowData.eq(2).text();
		
		gameboard.push(firstCell);
		gameboard.push(secondCell);
		gameboard.push(thirdCell);
		if (firstCell == secondCell &&
			secondCell == thirdCell &&
			thirdCell != "") {
				isWinner = true;
			}
		
	});
	
	//Vertical and diaganol checking... why can't we do this above? C'Mon! Think!
	if ((gameboard[0]== gameboard[3] && gameboard[3] == gameboard[6] && gameboard[0] != "")
		|| (gameboard[1]== gameboard[4] && gameboard[4] == gameboard[7] && gameboard[1] != "") 
		|| (gameboard[2]== gameboard[5] && gameboard[5] == gameboard[8] && gameboard[2] != "") 
		|| (gameboard[0]== gameboard[4] && gameboard[4] == gameboard[8] && gameboard[0] != "")
		|| (gameboard[2]== gameboard[4] && gameboard[4] == gameboard[6] && gameboard[2] != "")){
		isWinner = true;
	}
	
	return isWinner;
}

function canWinNow(column, player) {
	//We're going to pseduo add it to the game board and see if this move is a winner.
	var winner = false;
	if (column.text() == "") {
		//column.text(player).css("color", "white");
		winner = determineIfWin();
		//We want to change the column back to the way it was
		column.text("").css("color", "black");
	}
	
	if (winner) {
		alert("You betcha!");
	}
	return winner;
}

function getSpot(cellList) {
	var choices = [];
	$.each(cellList) {
		
	}
}
function doComputerMove(){
	var gameboard = [];
	var computerMove = null;
	/*Here's the logic we're going to institue:
	 * 1.) Can Comp Win this move?
	 * if no --
	 * 2.) Is there a possibility for the Player to Win next move?
	 * if no --
	 * 3.) Is a corner open?
	 * if no --
	 * 4.) Is center open?
	 * if no --
	 * 5.) Is side open?
	 * If no, the game is over.
	*/
	
	$("#board tr").each(function() {
		var rowData = $(this).find('td');
		var firstCell = rowData.eq(0);
		var secondCell = rowData.eq(1);
		var thirdCell = rowData.eq(2);
		
		canWinNow(firstCell, pieces.O);
		canWinNow(secondCell, pieces.O);
		canWinNow(thirdCell, pieces.O);
		canWinNow(firstCell, pieces.X);
		canWinNow(secondCell, pieces.X);
		canWinNow(thirdCell, pieces.X);
		
		
	});
	
}
