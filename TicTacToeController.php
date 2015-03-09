<?php

	session_start();
	include 'tictactoe.php';
	
	/**
 	* TicTacToe Controller. 
 	* @author Eric Blanks
	*/
	
 	if(!$_SESSION['tictactoe']) {
		$ticTacToe = new TicTacToe();
		$_SESSION['tictactoe'] = serialize($ticTacToe);
	} else {
		$ticTacToe = unserialize($_SESSION['tictactoe']);
	}

	switch($_POST['action']) {
		case "newGame" :
			$results = $ticTacToe->newGame();
			break;
		case "userMove" :
			$ticTacToe->changePlayer();
			$square = $_POST['square'];
			$x = substr($square, 0, 1);
    		$y = substr($square, 2, 1);
			$results = $ticTacToe->userMove($x, $y);
			break;
		case "computerMove" :
			$ticTacToe->changePlayer();
			$results = $ticTacToe->computerMove();
			break;
	}

	$_SESSION['tictactoe'] = serialize($ticTacToe);

	echo json_encode($results);
?>