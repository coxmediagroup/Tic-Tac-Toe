/*This file is intended to help clean up anything dealing with UI and to improve the user experience*/

//Variable Definitions

/* The following is quick way to check if we're using IE.
 * I can't take credit for this as I found this diddy at http://tinyurl.com/ldmzrg */
var IE = /*@cc_on!@*/false;
var piece = {X:'X', O:'O'}; 
var currentPiece = piece.X;
var endOfGame = false;
var clickCount = 0;

/*And here's where we disable selection for IE browsers.*/
if (IE) {
	window.onload = function() {
		document.getElementById('board').attachEvent('onselectstart', returnFalse);
	}
}

/*Initializes the game status text*/
function init() {
	changeGameStatus("Lay your first piece to begin!");
}

/*Sets the game status text based on the given string*/
function changeGameStatus(statusString) {
	$("#turn").text(statusString);
}

/*Some*/
function returnFalse()  
{
	return false;
}

/*Updates the the player who is up while game is not over. Otherwise, display the game winner.*/
function turnHandling() {
	if (!endOfGame) {
		currentPiece = (currentPiece == piece.X ? piece.O : piece.X);
		changeGameStatus("Game On, "+ currentPiece + "!");
		
	}
	else {
		changeGameStatus(currentPiece + " is the Winner!");
	}
}

/*Removes all pieces from the game board and resets all other necessary items to default*/
function clearGameBoard() {
	$("#board td").each(function() {
		$(this).text("");
	});
	currentPiece = piece.X;
	init();
	endOfGame = false;
	clickCount = 0;
}

/*This let's us know a cell has been clicked and then handles appropriately*/
$(document).ready(function() {
    $("#board td").click(function(e) {
		//this disallows a user from selecting a spot that's already filled in.
		if (!$(this).text() && !endOfGame)
		{
			$(this).text(currentPiece);
			endOfGame = determineIfWin();
			turnHandling();
			 if (clickCount == 4) {
				changeGameStatus("Game over! It's a cat's game!");
				endOfGame = true;
			}
			if (!endOfGame) {
				doComputerMove();
				endOfGame = determineIfWin();
				turnHandling();
			}
			clickCount++;
		} 
    });
});
