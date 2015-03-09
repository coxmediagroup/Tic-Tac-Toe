<?php
	session_start();
	include 'tictactoe.php';
	$ticTacToe = unserialize($_SESSION['tictactoe']);


	switch($_POST['action']) {
		case "newGame" :
			$results = $ticTacToe->newGame();
			break;
		case "userMove" :
			$ticTacToe->changePlayer();
			$results = $ticTacToe->userMove($_POST['square']);
			break;
		case "computerMove" :
			$ticTacToe->changePlayer();
			$results = $ticTacToe->computerMove();
			break;
	}

	$_SESSION['tictactoe'] = serialize($ticTacToe);

	echo json_encode($results);
?>