
/*
	Set the board to be ready for play.
*/
function setBoard(){

	//Determine if the game options are set to begin play
	var optionsAreEmpty = false;
	$('.control > option:selected').each(function( index, value ) {
  		if($(value).val()===''){
  			optionsAreEmpty=true;
  		} else{
  			if($(value).parent().prop('id') == 'human-piece'){
  				window.humanPiece = $(value).val();
  			}
  			if($(value).parent().prop('id') == 'first-player'){
  				window.firstPlayer = $(value).val();
	  			window.whoseTurn = $(value).val();
  			}
  		};
	});

	if(optionsAreEmpty){
		alert('Select game options first.');
		return;
	};

	//Set the visual cues that the board is ready
	$('#game-board td').css('cursor','pointer');
	$('#game-board td').css('background-color','#fff');
	$('#game-board td').css('border-color','#e7e7e7');

	//Disable options to prevent confusion if they are changed mid game
	$('.control').attr('disabled',true);
	$('#set-board').text('Game in Progress').attr('disabled',true);
	
	playGame();
}

/*
	Close the board for play
*/
function closeBoard(){
	//Set visual cues that the gameboard is not available
	$('#game-board td').css('cursor','not-allowed');
	$('#game-board td').css('background-color','#e7e7e7');
	$('#game-board td').css('border-color','#999');

	//Allow new options to be set for a new game
	$('.control').attr('disabled',false);
	$('#set-board').text('Play Again').attr('disabled',false);
}


/*
	Speed up development with debug feaures
*/
function devDebug(piece , player ){
		piece = piece || 'X';
		player = player || 'Human';
		$('#human-piece').val(piece);
		$('#first-player').val(player);
		setBoard();
}


function playGame(){
	gameMessage();
	
	
}

function gameMessage(){
	if(whoseTurn == 'Machine'){
		$('#message-cell').text('Machine is thinking');		
	} else{
		$('#message-cell').text('Human - it is your turn');
	}

}