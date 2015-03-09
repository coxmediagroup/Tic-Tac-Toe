function newGame() {
	var data = {
		"action" : "newGame"
	};
	
	/* start new sesssion */
	
	$.post( "TicTacToeController.php", data, function( data ) {
			
			var results = JSON.parse(data);
			
			$('#message').html('Please make your first move');
	});
}

function handleUserMove(divColumn) {
	
	var className = $("#" + divColumn.id).attr('class');

	if ($('#message').html().toUpperCase().indexOf('WINS') >= 0) {
		return false;
	}
	
	else if((className.indexOf('x-image') >= 0 || className.indexOf('o-image') >= 0)) {

		$('#message').html('Move already taken! Please try again.');

	}  else {

		$('#message').html('');
			
		var data = {
			"action" : "userMove",
			"square" : divColumn.id
		};

		$.post( "TicTacToeController.php", data, function( data ) {

				var results = JSON.parse(data);
				handleResults(results, true);
				$(divColumn).addClass(results.currentPlayer + '-image');
  			
		});
	}	
}

function handleResults(results, isUser) {
	if(results.winner != '-') {
		if(results.winner == 'c') {
			$('#message').html('Tie: No one wins');
		}
		else if(results.winner == 'x') {
			$('#message').html('Player 1 Wins!!!!');
		} else {
			$('#message').html('Player 2 (Computer) Wins!!!!');
		}
		player1Wins = results.stats.player1Wins;
		player2Wins = results.stats.player2Wins;
		drawWins = results.stats.drawWins;

		$('#stats').show();
		$('#total_games').html(player1Wins + player2Wins + drawWins);
		$('#player_1_wins').html(player1Wins);
		$('#player_2_wins').html(player2Wins);
		$('#draw_wins').html(drawWins);
		$('#play_again').show();

		drawWinner(results);
	} else {
		if(isUser) {
			computerPlay();
		}
	}
}

function drawWinner(results) {
	if(results.winData.col) {
		for(i = 0; i < 3; i++) {
			$('#' + i + '_' + results.winData.col).addClass('column_winner');
		}
	} else if(results.winData.row) {
		for(i = 0; i < 3; i++) {
			$('#' + results.winData.row + '_' + i).addClass('column_winner');
		}
	} else if(results.winData.diagnol1) {				
		$('#0_0').addClass('column_winner');
		$('#1_1').addClass('column_winner');
		$('#2_2').addClass('column_winner');
	} else if(results.winData.diagnol2) {
		$('#0_2').addClass('column_winner');
		$('#1_1').addClass('column_winner');
		$('#2_0').addClass('column_winner');
	}
}

function computerPlay() {
	//we have a winner
	var data = {
		"action" : "computerMove"
	};

	$.post( "TicTacToeController.php", data, function( data ) {

		var results = JSON.parse(data);
			$('#' + results.computerMove).addClass(results.currentPlayer + '-image');
  			
			handleResults(results);
	});
}

function clearBoard() {
	for(x = 0; x < 3; x++) {
		for(y = 0; y < 3; y++) {
			$('#' + x + '_' + y).html('');
			$('#' + x + '_' + y).removeClass('column_winner o-image x-image');
		}
	}

	$('#play_again').hide();
	$('#message').html('');
	newGame();
}