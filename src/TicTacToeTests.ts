/// <reference path="Game.ts" />
/// <reference path="Player.ts" />
/// <reference path="ComputerPlayer.ts" />
/// <reference path="HumanPlayer.ts" />

module TicTacToeTests {

	function displayResults(results:string, success:boolean) { 
		var color:string;
		(success) ? color = 'green' : color = 'red';
		var p = document.createElement("p");
		p.style.color = color;
		p.innerHTML = results;
		document
			.getElementById("testResults")
			.appendChild(p);
	}

	var game = new TicTacToe.Game();
	var humanPlayer = new TicTacToe.HumanPlayer();
	var computerPlayer = new TicTacToe.ComputerPlayer();
	
	humanPlayer.registerObserver(game);
	humanPlayer.registerObserver(computerPlayer);
	computerPlayer.registerObserver(game);

	// Test #1: Expect ComputerPlayer label to be 'Computer Player'.
	export function testOne() {
		var success:boolean;
		var results:string = 'Test #1: Expect ComputerPlayer label to be \'Computer Player\'';

		
		if (computerPlayer.getLabel() === 'Computer Player') {
			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}

		computerPlayer.reset();
		
		displayResults(results, success);
	}

	// Test #2: Expect HumanPlayer label to be 'Human Player'.
	export function testTwo() {
		var success:boolean;
		var results:string = 'Test #2: Expect HumanPlayer label to be \'Human Player\'';

		var humanPlayer = new TicTacToe.HumanPlayer();
		if (humanPlayer.getLabel() === 'Human Player') {
			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}
		
		displayResults(results, success);
	}

	// Test #3: Expect both players' initial score to be 0.
	export function testThree() {
		var success:boolean;
		var results:string = 'Test #3: Expect both players\' initial score to be 0';

		console.log('Human Player Score: ' + humanPlayer.getScore());
		console.log('Computer Player Score: ' + computerPlayer.getScore());

		if(humanPlayer.getScore() === 0 && computerPlayer.getScore() === 0) {
			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}

		computerPlayer.reset();
		
		displayResults(results, success);
	}

	// Test #4: If computer player has two in a row, expect computer player to play the third to get three in a row and win the game.
	export function testFour() {
		var success:boolean;
		var results:string = 'Test #4: If computer player has two in a row, expect computer player to play the third to get three in a row and win the game';

 		computerPlayer.makeMove(0);
 		humanPlayer.makeMove(1);
 		computerPlayer.makeMove(3); // computer player now has two in a row
 		humanPlayer.makeMove(7);
 		var moveIndex = computerPlayer.makeMove(); // should be 6 to complete the row and win the game

 		if(moveIndex === 6 && game.getWinner() && game.getWinner() === computerPlayer.getLabel()) { 
 			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}

		computerPlayer.reset();

		displayResults(results, success);

	}

	// Test #5: If human player has two in a row, expect computer player to play the third to block human player and win the game.
	export function testFive() {
		var success:boolean;
		var results:string = 'Test #5: If human player has two in a row, expect computer player to play the third to block human player and win the game';

		humanPlayer.makeMove(0);
 		computerPlayer.makeMove(1);
 		humanPlayer.makeMove(3); // human player has two in a row
 
 		var moveIndex = computerPlayer.makeMove();  // should be 6 to block human player
 		humanPlayer.makeMove(2);
 		computerPlayer.makeMove(7);
 		humanPlayer.makeMove(5);
 		var moveIndex2 = computerPlayer.makeMove(); // should be 8 to win the game

 		var winner = game.getWinner();

 		if(moveIndex === 6 && moveIndex2 === 8 && winner && winner === computerPlayer.getLabel()) { 
 			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}

		computerPlayer.reset();

		displayResults(results, success);

	}

	// Test #6: Expect computer player to create a forking opportunity where computer player can win in two ways and win the game.
	export function testSix() {
		var success:boolean;
		var results:string = 'Test #6: Expect computer player to create a forking opportunity where computer player can win in two ways and win the game';

		computerPlayer.makeMove(4);
		humanPlayer.makeMove(7);
		computerPlayer.makeMove(8);
		humanPlayer.makeMove(0); // blocks computer's first chance at winning
		var moveIndex = computerPlayer.makeMove(); // should be 5 to create a fork
		humanPlayer.makeMove(3);
		var moveIndex2 = computerPlayer.makeMove();  // should be 2 to win the game

 		var winner = game.getWinner(); 		

 		if(moveIndex === 5 && moveIndex2 === 2 && winner && winner === computerPlayer.getLabel()) { 
 			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}

		computerPlayer.reset();

		displayResults(results, success);

	}

	// Test #7: If human player has a fork or can fork, expect computer player to block human player's fork and win the game.
	export function testSeven() {
		var success:boolean;
		var results:string = 'Test #7: If human player has a fork or can fork, expect computer player to block human player\'s fork and win the game';

		

 		var winner = game.getWinner();
 		

 	// 	if(moveIndex === 5 && moveIndex2 === 2 && winner && winner === computerPlayer.getLabel()) { 
 	// 		success = true;
		// 	results += ' succeeded.';
		// } else {
		// 	success = false;
		// 	results += ' failed.';
		// }

		computerPlayer.reset();

		displayResults(results, success);
	}

	// Test #8: Expect computer player to play the center and win the game.

	// Test #9: If human player is in the corner, expect computer player to play the opposite corner and win the game.

	// Test #10: Expect computer player to play an empty corner and win the game.

	// Test #11: Expect computer player to play an empty side and win the game.

	// Test #12: Expect nextPlayer to be human player after computer player has made a move.

	// Test #13: Expect nextPlayer to be computer player after human player has made a move.

	// Test #14: Expect score to be updated after each round.
}

TicTacToeTests.testOne();
TicTacToeTests.testTwo();
TicTacToeTests.testThree();
TicTacToeTests.testFour();
TicTacToeTests.testFive();
TicTacToeTests.testSix();
TicTacToeTests.testSeven();
// TicTacToeTests.testEight();
// TicTacToeTests.testNine();
// TicTacToeTests.testTen();
// TicTacToeTests.testEleven();
// TicTacToeTests.testTwelve();
// TicTacToeTests.testThirteen();
// TicTacToeTests.testFourteen();