(function(){
	var compFirstMove = -1;
	playGame();

	function playGame(){
		// -1 means computer won, 1 means player won, 2 means tie
		var winner = 0;
		var gameBoard = new Array();

		gameBoard[0] = 0;
		gameBoard[1] = 0;
		gameBoard[2] = 0;

		gameBoard[3] = 0;
		gameBoard[4] = 0;
		gameBoard[5] = 0;

		gameBoard[6] = 0;
		gameBoard[7] = 0;
		gameBoard[8] = 0;
		updateBoard(gameBoard);
		$(".alert").remove();

		$("#button-0").on("click", function(event){
			if(gameBoard[0] == 0);
			gameBoard[0] = 1;
			processGameFrame();
		});
		$("#button-1").on("click", function(event){
			if(gameBoard[1] == 0);
			gameBoard[1] = 1;
			processGameFrame();
		});
		$("#button-2").on("click", function(event){
			if(gameBoard[2] == 0);
			gameBoard[2] = 1;
			processGameFrame();
		});

		$("#button-3").on("click", function(event){
			if(gameBoard[3] == 0);
			gameBoard[3] = 1;
			processGameFrame();
		});
		$("#button-4").on("click", function(event){
			if(gameBoard[4] == 0);
			gameBoard[4] = 1;
			processGameFrame();
		});
		$("#button-5").on("click", function(event){
			if(gameBoard[5] == 0);
			gameBoard[5] = 1;
			processGameFrame();
		});

		$("#button-6").on("click", function(event){
			if(gameBoard[6] == 0);
			gameBoard[6] = 1;
			processGameFrame();
		});
		$("#button-7").on("click", function(event){
			if(gameBoard[7] == 0);
			gameBoard[7] = 1;
			processGameFrame();
		});
		$("#button-8").on("click", function(event){
			if(gameBoard[8] == 0);
			gameBoard[8] = 1;
			processGameFrame();
		});
	
		function processGameFrame(){
			winner = checkGameOver(gameBoard, 1);
			updateBoard(gameBoard);
			if(winner == 0){
				gameBoard = getComputerMove(gameBoard);
				winner = checkGameOver(gameBoard, -1);
				updateBoard(gameBoard);
				if(winner != 0){
					displayWinner(winner);
				}
			} else {
				displayWinner(winner);
			}
		}
	}

	function displayWinner(winner){
		if(winner == -1){
			$('body').prepend('<div class="alert alert-error">Computer Wins</div>');
		} else if(winner == 1){
			$('body').prepend('<div class="alert alert-success">You Win!</div>');
		} else {
			$('body').prepend('<div class="alert">Cat game, no one wins</div>');
		}
	}

	function getComputerMove(gameBoard){
		var localBoard;
		// try to win first
		localBoard = tryToWinOrBlock(gameBoard, -1);
		if(localBoard){
			return localBoard;
		}

		// try to block player from winning
		localBoard = tryToWinOrBlock(gameBoard, 1);
		if(localBoard){
			return localBoard;
		}

		// pick middle
		if(gameBoard[4] == 0){
			gameBoard[4] = -1;
			if(compFirstMove == -1){
				compFirstMove = 4;
			}
			return gameBoard;
		}

		// pick a corner except when first move was the center
		if(compFirstMove == 4){
			if(gameBoard[1] == 0){
				gameBoard[1] = -1;
				return gameBoard;
			} else if(gameBoard[3] == 0){
				gameBoard[3] = -1;
				return gameBoard;
			} else if(gameBoard[5] == 0){
				gameBoard[5] = -1;
				return gameBoard;
			} else if(gameBoard[7] == 0){
				gameBoard[7] = -1;
				return gameBoard;
			}
		} else {
			if(gameBoard[0] == 0){
				gameBoard[0] = -1;
				if(compFirstMove == -1){
					compFirstMove = 0;
				}
				return gameBoard;
			} else if(gameBoard[2] == 0){
				gameBoard[2] = -1;
				return gameBoard;
			} else if(gameBoard[6] == 0){
				gameBoard[6] = -1;
				return gameBoard;
			} else if(gameBoard[8] == 0){
				gameBoard[8] = -1;
				return gameBoard;
			}
		}

		// pick a remaining spot
		if(gameBoard[1] == 0){
			gameBoard[1] = -1;
			return gameBoard;
		} else if(gameBoard[3] == 0){
			gameBoard[3] = -1;
			return gameBoard;
		} else if(gameBoard[5] == 0){
			gameBoard[5] = -1;
			return gameBoard;
		} else if(gameBoard[7] == 0){
			gameBoard[7] = -1;
			return gameBoard;
		}
	}

	function tryToWinOrBlock(gameBoard, player){
		// top row
		if(gameBoard[0] == player && gameBoard[1] == player && gameBoard[2] == 0){
			gameBoard[2] = -1;
		} else if(gameBoard[0] == player && gameBoard[2] == player && gameBoard[1] == 0){
			gameBoard[1] = -1;
		} else if(gameBoard[1] == player && gameBoard[2] == player && gameBoard[0] == 0){
			gameBoard[0] = -1;
		}
		// middle row
		else if(gameBoard[3] == player && gameBoard[4] == player && gameBoard[5] == 0){
			gameBoard[5] = -1;
		} else if(gameBoard[3] == player && gameBoard[5] == player && gameBoard[4] == 0){
			gameBoard[4] = -1;
		} else if(gameBoard[4] == player && gameBoard[5] == player && gameBoard[3] == 0){
			gameBoard[3] = -1;
		}
		// bottom row
		else if(gameBoard[6] == player && gameBoard[7] == player && gameBoard[8] == 0){
			gameBoard[8] = -1;
		} else if(gameBoard[6] == player && gameBoard[8] == player && gameBoard[7] == 0){
			gameBoard[7] = -1;
		} else if(gameBoard[7] == player && gameBoard[8] == player && gameBoard[6] == 0){
			gameBoard[6] = -1;
		}
		// left column
		else if(gameBoard[0] == player && gameBoard[3] == player && gameBoard[6] == 0){
			gameBoard[6] = -1;
		} else if(gameBoard[0] == player && gameBoard[6] == player && gameBoard[3] == 0){
			gameBoard[3] = -1;
		} else if(gameBoard[3] == player && gameBoard[6] == player && gameBoard[0] == 0){
			gameBoard[0] = -1;
		}
		// middle column
		else if(gameBoard[1] == player && gameBoard[4] == player && gameBoard[7] == 0){
			gameBoard[7] = -1;
		} else if(gameBoard[1] == player && gameBoard[7] == player && gameBoard[4] == 0){
			gameBoard[4] = -1;
		} else if(gameBoard[4] == player && gameBoard[7] == player && gameBoard[1] == 0){
			gameBoard[1] = -1;
		}
		// right column
		else if(gameBoard[2] == player && gameBoard[5] == player && gameBoard[8] == 0){
			gameBoard[8] = -1;
		} else if(gameBoard[2] == player && gameBoard[8] == player && gameBoard[5] == 0){
			gameBoard[5] = -1;
		} else if(gameBoard[5] == player && gameBoard[8] == player && gameBoard[2] == 0){
			gameBoard[2] = -1;
		}
		// diagonal left to right
		else if(gameBoard[0] == player && gameBoard[4] == player && gameBoard[8] == 0){
			gameBoard[8] = -1;
		} else if(gameBoard[0] == player && gameBoard[8] == player && gameBoard[4] == 0){
			gameBoard[4] = -1;
		} else if(gameBoard[4] == player && gameBoard[8] == player && gameBoard[0] == 0){
			gameBoard[0] = -1;
		}
		// diagonal right to left
		else if(gameBoard[2] == player && gameBoard[4] == player && gameBoard[6] == 0){
			gameBoard[6] = -1;
		} else if(gameBoard[2] == player && gameBoard[6] == player && gameBoard[4] == 0){
			gameBoard[4] = -1;
		} else if(gameBoard[4] == player && gameBoard[6] == player && gameBoard[2] == 0){
			gameBoard[2] = -1;
		}

		else {
			return false;
		}

		return gameBoard;
	}

	function checkGameOver(gameBoard, player){
		// top row
		if(gameBoard[0] == player && gameBoard[1] == player && gameBoard[2] == player){
			return player;
		}
		// middle row
		else if(gameBoard[3] == player && gameBoard[4] == player && gameBoard[5] == player){
			return player;
		}
		// bottom row
		else if(gameBoard[6] == player && gameBoard[7] == player && gameBoard[8] == player){
			return player;
		}
		// left column
		else if(gameBoard[0] == player && gameBoard[3] == player && gameBoard[6] == player){
			return player;
		}
		// middle column
		else if(gameBoard[1] == player && gameBoard[4] == player && gameBoard[7] == player){
			return player;
		}
		// right column
		else if(gameBoard[2] == player && gameBoard[5] == player && gameBoard[8] == player){
			return player;
		}
		// diagonal left to right
		else if(gameBoard[0] == player && gameBoard[4] == player && gameBoard[8] == player){
			return player;
		}
		// diagonal right to left
		else if(gameBoard[2] == player && gameBoard[4] == player && gameBoard[6] == player){
			return player;
		} else {
			if(movesLeft(gameBoard)){
				return 0;
			} else {
				return 2;
			}
		}
	}

	function movesLeft(gameBoard){
		if(gameBoard[0] && gameBoard[1] && gameBoard[2]
			&& gameBoard[3] && gameBoard[4] && gameBoard[5]
			&& gameBoard[6] && gameBoard[7] && gameBoard[8]){
			return false;
		} else {
			return true;
		}
	}

	function updateBoard(gameBoard){
		setSpot(gameBoard[0], '#button-0');
		setSpot(gameBoard[1], '#button-1');
		setSpot(gameBoard[2], '#button-2');

		setSpot(gameBoard[3], '#button-3');
		setSpot(gameBoard[4], '#button-4');
		setSpot(gameBoard[5], '#button-5');

		setSpot(gameBoard[6], '#button-6');
		setSpot(gameBoard[7], '#button-7');
		setSpot(gameBoard[8], '#button-8');
	}

	function setSpot(spot, selector){
		if(spot == -1){
			$(selector).text('X');
		} else if(spot == 1) {
			$(selector).text('O');
		}
	};
})();