/* This file is for anything and everything dealing with actual game play */

function determineIfWin() {
	//Right, so the below logic isn't enitrely awesome.
	//Should improve on it at some point
	
	/* The "each" stuff essentially is checking if there are any
	 * matches horizontally while also building up a list to check
	 * for other directional matches later */
	var gameboard = [];
	var isWinner = null;
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
	var winner = null;
	if (column.text() == "") {
		column.text(player).css("color", "white");
		winner = determineIfWin();
		//We want to change the column back to the way it was
		column.text("").css("color", "black");
	}
	
	if (winner) {
		alert("You betcha!");
	}
	return winner;
}

/* Attempts to determine next open spot to be played. 
 * If a spot can't be found, null is returned. */
function getSpot(cellList) {
	var choices = [];
	var cLength = -1;
	
	cLength = choices.length;
	return (cLength > 0 ? choices[Math.floor(Math.random*cLength - 1)] : null);
}

function doComputerMove(){
	/*Here's the logic we're going to institute:
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
	
	var computerMove = null;
	var corners = [0,2,6,8];
	var sides = [3,5];
	var center = [4];
	var ends = [0,2];
	
	$("#board td").each(function() {
		computerMove = (canWinNow($(this), piece.O) ? canWinNow(cell, piece.O) : null);
		
		if (!computerMove)
			computerMove = (canWinNow($(this), piece.X) ? canWinNow(cell, piece.X) : null);
		
		if ($.inArray($(this).parent().index(), ends)) 
		{
			if ($.inArray($(this).index(), ends)) {
				//Get the Corners
			    corners.push($(this));
			}
			else if ($(this).index() == 1) {
				//Get the Sides Piece
				sides.push($(this));
			}
		}
		
		else if ($(this).parent().index() == 1) 
		{
			if ($.inArray($(this).index(), ends)) {
				//Get the Sides
				sides.push($(this));
			}
			else if ($(this).index() == 1) {
				//Get the Center
				center = $(this);
			}
		
	});
	
	alert(corners.length);
	alert(corners);
	
	if (!computerMove)
		computerMove = (getSpot(corners) != null ? getSpot(corners) : null);
	if (!computerMove)
		computerMove = (getSpot(center) != null ? getSpot(center) : null);
	if (!computerMove)
		computerMove = (getSpot(sides) != null ? getSpot(sides) : null);
	
	alert("here" + computerMove);
	alert(computerMove.text());
	if (computerMove) {
		computerMove.text(piece.O);
	}
}
