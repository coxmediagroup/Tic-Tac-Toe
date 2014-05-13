var playerIndicator = Math.floor(Math.random()*2)+1;

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
			$(selector).off();
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
	//setup board, get or create a board based on email address
	var jqxhr = $.get('/api/board', function(data){
		updateBoard(data);
	});
}
function initBoard(){
	//apply button listeners
	$('.board-row-cell').click(function(){
		id = $(this).attr('id');
		toggleBoard(id);
		return false;
	})
	//hide the alerts which indicate ties and loss
	$('#loss-alert').hide();
	$('#tie-alert').hide();
	togglePlayerIndictator();
	setupBoard();
	startGame();
}
function startGame(){
	if (playerIndicator==2){
		$.get('/api/cpuplay', function(data){
			updateBoard(data);
			togglePlayerIndictator();
		});
	}
}
function newGame(){
	playerIndicator = Math.floor(Math.random()*2)+1;
	console.log(playerIndicator);
	$.get('/api/newGame', function(data){
		initBoard();
	});
}
function togglePlayerIndictator(){
	if(playerIndicator==1){
		$('.player-turn').removeClass('selected');
		$('.cpu-turn').addClass('selected');
		$('.player-turn').hide();
		$('.cpu-turn').show();
		playerIndicator = 2;
	}else if(playerIndicator==2){
		$('.cput-turn').removeClass('selected');
		$('.player-turn').addClass('selected');
		$('.cpu-turn').hide();
		$('.player-turn').show();
		playerIndicator = 1;
	}
}