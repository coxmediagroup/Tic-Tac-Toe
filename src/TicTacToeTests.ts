/// <reference path="TicTacToe.ts" />
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

	// Test #1: Expect ComputerPlayer label to be 'Computer Player'.
	export function testOne() {
		var success:boolean;
		var results:string = 'Test #1: Expect ComputerPlayer label to be \'Computer Player\'';

		var computerPlayer = new TicTacToe.ComputerPlayer();
		if (computerPlayer.getLabel() === 'Computer Player') {
			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}
		
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

		var humanPlayer = new TicTacToe.HumanPlayer();
		var computerPlayer = new TicTacToe.ComputerPlayer();

		console.log('Human Player Score: ' + humanPlayer.getScore());
		console.log('Computer Player Score: ' + computerPlayer.getScore());

		if(humanPlayer.getScore() === 0 && computerPlayer.getScore() === 0) {
			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}
		
		displayResults(results, success);
	}
}

TicTacToeTests.testOne();
TicTacToeTests.testTwo();
TicTacToeTests.testThree();
