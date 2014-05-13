var firstPlayer = Math.floor(Math.random()*2)+1;

function toggleBoard(cell){
	var selector = "#"+cell;
	togglePlayerIndictator();
	if($(selector).hasClass('selected')){
	}
	else {
		$(selector).text("O");
		$(selector).addClass('selected');
		var jqxhr = $.get('/api/play/'+cell, function(data){
			//console.log(data['board']);
			updateBoard(data);
			togglePlayerIndictator();
		});
	}
}
function updateBoard(data){
	board = data['board'];
	for(i=0; i<board.length; i++){
		if(board[i]==1){
			$('#'+i).text('O');
			$('#'+i).addClass('selected');
		} else if (board[i]==2){
			$('#'+i).text('X');
			$('#'+i).addClass('selected');
		} else {
			$('#'+i).text('');
			$('#'+i).removeClass('selected');
		}
	}
	if (data['isWin'] == true){
		$('#loss-alert').show();
	} else if (data['isTie'] == true){
		$('#tie-alert').show();
	}
}
function setupBoard(){
	//Hide or show player indicator
	$('.player-indicator').hide();
	if (firstPlayer==1){
		$('.player-turn').show();
		$('.player-turn').addClass('selected');
	}else{
		$('.cpu-turn').show();
		$('.cpu-turn').addClass('selected');
		var jqxhr = $.get('/api/cpuplay', function(data){
			updateBoard(data);
			togglePlayerIndictator();
		});
	}
	
	//hide the alerts which indicate ties and loss
	$('#loss-alert').hide();
	$('#tie-alert').hide();
	
	//setup board, get or create a board based on email address
	var jqxhr = $.get('/api/board', function(data){
		updateBoard(data);
	});
}
function togglePlayerIndictator(){
	if($('.player-turn').hasClass('selected')){
		$('.player-turn').removeClass('selected');
		$('.cpu-turn').addClass('selected');
		$('.player-turn').hide();
		$('.cpu-turn').show();
	}else if($('.cpu-turn').hasClass('selected')){
		$('.cput-turn').removeClass('selected');
		$('.player-turn').addClass('selected');
		$('.cpu-turn').hide();
		$('.player-turn').show();
	}
}
function newGame(){
	firstPlayer = Math.floor(Math.random()*2)+1;
	$('#loss-alert').hide();
	$('#tie-alert').hide();
	var jqxhr = $.get('/api/newGame', function(data){
		updateBoard(data);
	});
}