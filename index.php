<?php

	session_start();
	$sessionId = session_id ();
	echo("sessionId=" + $sessionId);
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
   			<div class="column" id="square_1" onclick=handleUserMove(this)></div>
   			<div class="column" id="square_2" onclick=handleUserMove(this)></div>
   			<div class="column" id="square_3" onclick=handleUserMove(this)></div>
		</div>
		<div class="row" id="row2">
   			<div class="column" id="square_4" onclick=handleUserMove(this)></div>
   			<div class="column" id="square_5" onclick=handleUserMove(this)></div>
   			<div class="column" id="square_6" onclick=handleUserMove(this)></div>
		</div>
		<div class="row" id="row3">
   			<div class="column" id="square_7" onclick=handleUserMove(this)></div>
   			<div class="column" id="square_8" onclick=handleUserMove(this)></div>
   			<div class="column" id="square_9" onclick=handleUserMove(this)></div>
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
    	/* start new sesssion */
	}); 

	function handleUserMove(divColumn) {

		if($(divColumn).text().length != 0) {
			$('#message').html('Move already taken! Please try again.');

		} else {
			$(divColumn).html('X');

			//we have a winner
			var data = {
				"sessionId" : "<?php echo($sessionId)?>",
				"action" : "move",
				"square" : divColumn.id
			};

			//var results = $ticTacToe->processRequest(data);

			//console.log(results);
			//$(divColumn).addClass('column_winner');
			//$('#play_again').show();
			
			$.post( "tictactoe.php", data, function( data ) {
  				alert( "Data Loaded: " + data );
			});

		}
	}

	function clearBoard() {
		for(i=1; i <= 9; i++) {
			$('#square_' + i).html('');
			$('#square_' + i).removeClass('column_winner');
		}

		$('#play_again').hide();
	}
</script>