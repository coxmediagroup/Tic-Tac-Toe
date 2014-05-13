function toggleBoard(cell){
	var selector = "#"+cell;
	
	if($(selector).hasClass('selected')){
		//$(selector).text("");
		//$(selector).removeClass('selected');
	}
	else {
		$(selector).text("O");
		$(selector).addClass('selected');
		var jqxhr = $.get('/api/play/'+cell, function(data){
			//console.log(data['board']);
			updateBoard(data);
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
	var jqxhr = $.get('/api/board', function(data){
		updateBoard(data);
	});
}
function newGame(){
	$('#loss-alert').hide();
	$('#tie-alert').hide();
	var jqxhr = $.get('/api/newGame', function(data){
		updateBoard(data);
	});
}