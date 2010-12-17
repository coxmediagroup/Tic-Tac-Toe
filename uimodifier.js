/*This file is intended to help clean up anything dealing with UI and to improve the user experience*/

//Global Variable Definitions

/* Er, um, what?!?!? The following is quick way to check if we're using IE.
 * Why? Well, the window.onload statement would throw up an error if we were using
 * some sort of legit browser like (but not limited to) Chrome, Firefox, or Safari.
 * I can't take credit for this as I found this diddy at http://tinyurl.com/ldmzrg */
var IE = /*@cc_on!@*/false;
var piece = {X:'X', O:'O'}; 
var currentPiece = piece.X;
var endOfGame = false;
var clickCount = 0;

function init() {
	changeGameStatus(currentPiece + " is up");
}

function changeGameStatus(statusString) {
	$("#turn").text(statusString);
}
/* Why are we doing this? Because we need to attach a function later 
 * on to disallow selection
 * across multiple browsers including IE6. */ 
function returnFalse()  
{
	return false;
}

/*And here's where we disable selection for IE browsers.*/
if (IE) {
	window.onload = function() {
		document.getElementById('board').attachEvent('onselectstart', returnFalse);
	}
}

function turnHandling() {
	if (!endOfGame) {
		currentPiece = (currentPiece == piece.X ? piece.O : piece.X);
		changeGameStatus(currentPiece + " is up");
	}
	else {
		changeGameStatus(currentPiece + " is the Winner!");
	}
}

function clearGameBoard() {
	$("#board td").each(function() {
		$(this).text("");
	});
	currentPiece = piece.X;
	changeGameStatus(currentPiece + " is up");
	endOfGame = false;
	clickCount = 0;
}

/*This let's us know a cell has been clicked. So, er, um, yeah, it means do something!*/
$(document).ready(function() {
    $("#board td").click(function(e) {
		//this disallows a user from selecting a spot that's already filled in.
		if (!$(this).text() && !endOfGame)
		{
			$(this).text(currentPiece);
			determineIfWin();
			turnHandling();
			 if (clickCount == 8) {
				changeGameStatus("Game over! It's a cat's game!")
			}
			clickCount++;
		} 
        //alert($(this).parent().index() + " " + $(this).parent().children().index($(this)));
    });
});
