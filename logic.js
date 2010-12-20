/* This file is for anything and everything dealing with actual game play */

function determineIfWin() {
	//Right, so the below logic isn't enitrely awesome.
	//Should improve on it at some point
	
	/* The "each" stuff essentially is checking if there are any
	 * matches horizontally while also building up a list to check
	 * for other directional matches later */
	var gameboard = [];
	var isWinner = null;
	var rowData = null;
	var first = null;
	var second = null;
	var third = null;
	//Don't initialize a variable each time through the loop! Go through and fix!
	$("#board tr").each(function() {
		rowData = $(this).find('td');
		first = rowData.eq(0).text();
		second = rowData.eq(1).text();
		third = rowData.eq(2).text();
		
		gameboard.push(first);
		gameboard.push(second);
		gameboard.push(third);
		if (first == second &&
			second == third &&
			third != "") {
				isWinner = true;
			}
		
	});
	
	//Vertical and diaganol checking... 
	if ((gameboard[0]== gameboard[3] && gameboard[3] == gameboard[6] && gameboard[0] != "")
		|| (gameboard[1]== gameboard[4] && gameboard[4] == gameboard[7] && gameboard[1] != "") 
		|| (gameboard[2]== gameboard[5] && gameboard[5] == gameboard[8] && gameboard[2] != "") 
		|| (gameboard[0]== gameboard[4] && gameboard[4] == gameboard[8] && gameboard[0] != "")
		|| (gameboard[2]== gameboard[4] && gameboard[4] == gameboard[6] && gameboard[2] != "")){
		isWinner = true;
	}
	
	return isWinner;
}

/*Checks to see if the given player can win on the given move.*/
function canWinNow(column, player) {
	//We're going to pseudo add it to the game board and see if this move is a winner.
	var winner = null;
	if (column.text() == "") {
		column.text(player).css("color", "white");
		winner = determineIfWin();
		//We want to change the column back to the way it was
		column.text("").css("color", "black");
	}
	return winner;
}

/* Attempts to determine next open spot to be played. 
 * If a spot can't be found, null is returned. */
function getSpot(cellList) {
	var cLength = -1;
	cLength = cellList.length;
	return (cLength > 0 ? cellList[Math.floor(Math.random() * cLength)] : null);
}

/* Lays computer's piece based on the given location 
 * (which is in the format of [row, col])*/
function makeMove(location) {
		$("#board tr td").each(function() {
			if ($(this).parent().index() == location[0] 
				&& $(this).index() == location[1]) {
				$(this).text(piece.O);
			}
		});
}

/* Returns best location when two corner pieces are in play*/
function checkDiag(cornerList) {
	if (cornerList[0][0] != cornerList[1][0] && cornerList[0][1] != cornerList[1][1]) {
		return [1, cornerList[1][1]];
	} 
}

/* Removes any open cells from our available cell list that 
 * could potentially lead to a computer loss*/
function removeBadMove(oldList, sides, compList) {
	var rowCounts = [0,0,0];
	var tempList = [];
	
	if (sides) 
	{
		tempList = oldList;
		oldList = compList;
	}
	for (var i = 0; i < oldList.length; i++) {
		if (oldList[i][0] == 0)
			rowCounts[0]++;
		else if (oldList[i][0] == 1)
			rowCounts[1]++;
		else if (oldList[i][0] == 2)
			rowCounts[2]++;
	}

	
	var delRow = null;
	if (sides)
	{
		oldList = tempList;
		tempList = [];
		
		if (rowCounts[0]  > rowCounts[1] -1 && rowCounts[0] > rowCounts[2])
			delRow = 0;
		else if (rowCounts[1] -1  > rowCounts[2] && rowCounts[1] -1 > rowCounts[0])
			delRow = 1;
		else if (rowCounts[2]  > rowCounts[0] && rowCounts[2] > rowCounts[1] -1)
			delRow = 2;
	}
	else {
		if (rowCounts[0]  < rowCounts[2] )
			delRow = 0;
		else if (rowCounts[2]  < rowCounts[0])
			delRow = 2;
	}
	
	for (var i = 0; i < oldList.length; i++) {
			if (oldList[i][0] != delRow)
			{
				tempList.push(oldList[i]);
		}
	}
	return tempList;
}

/* Calculates and carries out the computer's move based on where the player's pieces 
	currently are and what is available.*/
function doComputerMove(){
	
	var moveCheck = null;
	var corners = [];
	var sides = [];
	var center = [];
	var ends = [0,2];
	var nextMove = null;
	var row = null;
	var col = null;
	var cellText = null;
	var cornerList = [];
	var pieceList = [];
	
	$("#board tr td").each(function() {
		row = $(this).parent().index();
		col = $(this).index();
		
		//Wins are found, let's just return and not check other pieces.
		moveCheck = (canWinNow($(this), piece.O) ? 
			[row, col] : null);

		if (moveCheck) { nextMove = moveCheck; return; }
		
		if (!moveCheck)
			moveCheck = (canWinNow($(this), piece.X) ? 
				[row, col] : null)
		
		if (moveCheck) { nextMove = moveCheck; return; }
		
		cellText = $(this).text();
		
		//Let's figure out where all spots are empty.
		if ($.inArray(row, ends) > -1 && cellText =="") 
		{
			if ($.inArray(col, ends) > -1) 
			    corners.push([row, col]);
			else if (col == 1) 
				sides.push([row, col]);	
		}
	
		else if (row == 1 && cellText =="") 
		{
			if ($.inArray(col, ends) > -1) 
				sides.push([row, col]);
			
			else if (col == 1) 
				center.push([row, col]);	
		}

		/*If this is a corner piece and it's an X, let's save it for later*/
		if ($.inArray(row, ends) > -1 && $.inArray(col, ends) > -1
			&& $(this).text() == piece.X) 
				cornerList.push([row, col]);
	});
	
	//Checks to see if 
	if (!nextMove && cornerList.length == 2)
	    nextMove = checkDiag(cornerList);
	if (!nextMove && cornerList.length == 1 && corners.length == 3)
		corners = removeBadMove(corners, false);		
	if (!nextMove && sides.length == 2) 
		corners = removeBadMove(corners, true, sides);
	
	pieceList = [center, corners, sides];
	for (var i = 0; i < pieceList.length; i++)
	{
		if (!nextMove)
			nextMove = getSpot(pieceList[i]);
	}

	if (nextMove) 
		makeMove(nextMove);
}
