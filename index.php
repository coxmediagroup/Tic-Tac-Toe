<html>
	<head>
       <link rel="stylesheet" type="text/css" href="./css/tictactoe.css">
	</head>
	<body>
	<div id="game">	
		<div id="center">
		<img src="./images/logo.png"/>
		<h1>Tic Tac Toe</h1>
		<div id="message" class="message"></div>
		<div class="board">
		<?php
			// draw 3x3 tic tac toe board
			for($x = 0; $x< 3; $x++) {
				echo('<div class="row" id="row' .($x+1) ."\">\n");

				for($y = 0; $y < 3; $y++) {
					echo('<div class="column" id="' .$x .'_' .$y ."\" onclick=handleUserMove(this)></div><div style=\"width=10px;float:left\"></div>\n");
				}
				echo('</div>');
			}
		?>
	</div>
		
		<div id="play_again">
			<input type="button" name="play_again" value="Play Again" class="button" onclick=clearBoard()>
		</div>
		<div id="stats" style="display:none">
			<div class="row">
				<div class="column_title">Total Games</div>
				<div class="column_title">Player 1</div>
				<div class="column_title">Player 2</div>
				<div class="column_title">Draw</div>
			</div>
			<div class="row">
				<div class="column_data" id="total_games"></div>
				<div class="column_data" id="player_1_wins"></div>
				<div class="column_data" id="player_2_wins"></div>
				<div class="column_data" id="draw_wins"></div>
			</div>
		</div>
	</div>	
	</div>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
	<script src="./js/tictactoe.js"></script>
	<script>
		$(document).ready(function() {

	    	newGame();
		}); 
	</script>
	</body>
</html>

