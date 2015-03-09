<?php
	session_start();
	include 'tictactoe.php';
	$ticTacToe = new TicTacToe();
	$_SESSION['tictactoe'] = serialize($ticTacToe);
?>

<html>
	<head>
<style>
body {
    background-color: linen;
}
h1 {
    color: maroon;
    margin-left: 40px;
} 
.row{
	background-color: #bbb;
}

.row:after {
    content: "";
    clear: both;
    display: block;
}

.column{
	
	float: left;
	height:90px;
	width:90px;
	background-color: #FF1493;
	padding:10 10 0 0;
}

.column_winner{
	background-color: yellow;
}

#play_again{
	display: none;
}

</style>
	</head>
	<body>
		<h1>Tic Tac Toe</h1>
		<div id="message"></div>
		<div class="row" id="row1">
   			<div class="column" id="0_0" onclick=handleUserMove(this)></div>
   			<div class="column" id="0_1" onclick=handleUserMove(this)></div>
   			<div class="column" id="0_2" onclick=handleUserMove(this)></div>
		</div>
		<div class="row" id="row2">
   			<div class="column" id="1_0" onclick=handleUserMove(this)></div>
   			<div class="column" id="1_1" onclick=handleUserMove(this)></div>
   			<div class="column" id="1_2" onclick=handleUserMove(this)></div>
		</div>
		<div class="row" id="row3">
   			<div class="column" id="2_0" onclick=handleUserMove(this)></div>
   			<div class="column" id="2_1" onclick=handleUserMove(this)></div>
   			<div class="column" id="2_2" onclick=handleUserMove(this)></div>
		</div>
		<div>
			<input type="button" name="play_again" id="play_again" value="Play Again" class="button" onclick=clearBoard()>
		</div>
	</body>
</html>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script>

	$(document).ready(function() {
    	console.log("doc ready");
    	newGame();
		
	}); 

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

		if ($('#message').html().toUpperCase().indexOf('WINS') >= 0) {
			return false;
		}
		else if($(divColumn).text().length != 0) {
			$('#message').html('Move already taken! Please try again.');

		}  else {
			
			//we have a winner
			var data = {
				"action" : "userMove",
				"square" : divColumn.id
			};

			$.post( "TicTacToeController.php", data, function( data ) {

  				var results = JSON.parse(data);
  				handleResults(results, true);
  				$(divColumn).html(results.currentPlayer);

	  			
	  			console.log('results=');
	  			console.log(results);
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
			$('#play_again').show();
		} else {
			if(isUser) {
				computerPlay();
			}
		}
	}

	function computerPlay() {
		//we have a winner
		var data = {
			"action" : "computerMove"
		};

		$.post( "TicTacToeController.php", data, function( data ) {

			var results = JSON.parse(data);

			console.log('!!!!!!!!!!!!!!!COMPUTER MOVE results=');
  			console.log(results);

  			$('#' + results.computerMove).html(results.currentPlayer);

  			handleResults(results);
		});

	}

	function clearBoard() {
		for(x = 0; x < 3; x++) {
			for(y = 0; y < 3; y++) {
				$('#' + x + '_' + y).html('');
				$('#' + x + '_' + y).removeClass('column_winner');
			}
		}

		$('#play_again').hide();
		$('#message').html('');
		newGame();
	}

	function disableBoard() {
		alert('in disable');
		for(x = 0; x < 3; x++) {
			for(y = 0; y < 3; y++) {
				$('#' + x + '_' + y).unbind('onclick click');
			}
		}
	}
</script>