
/*
	Set the board to be ready for play.
*/
function setBoard(){

	//Determine if the game options are set to begin play
	var optionsAreEmpty = false;
	$('.control > option:selected').each(function( index, value ) {
  		if($(value).val()===''){
  			optionsAreEmpty=true;
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
}

/*
	Close the board for play
*/
function closeBoard(){
	$('#game-board td').css('cursor','not-allowed');
	$('#game-board td').css('background-color','#e7e7e7');
	$('#game-board td').css('border-color','#999');
}

