
/*
	Set the board to be ready for play.
*/
function setBoard(){
	//Set the visual cues that the board is ready
	$('#game-board td').css('cursor','pointer');
	$('#game-board td').css('background-color','#fff');
	$('#game-board td').css('border-color','#e7e7e7');
}

/*
	Close the board for play
*/
function closeBoard(){
	$('#game-board td').css('cursor','not-allowed');
	$('#game-board td').css('background-color','#e7e7e7');
	$('#game-board td').css('border-color','#999');
}