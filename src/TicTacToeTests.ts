/// <reference path="TicTacToe.ts" />
/// <reference path="ComputerPlayer.ts" />
/// <reference path="HumanPlayer.ts" />

module TicTacToeTests {

	export function displayResults(results:string, success:boolean) { 
		var color:string;
		(success) ? color = 'green' : color = 'red';
		var p = document.createElement("p");
		p.style.color = color;
		p.innerHTML = results;
		document
			.getElementById("testResults")
			.appendChild(p);
	}

	// Test #1: Expect ComputerPlayer label to be 'Computer Player'
	export function testOne() {
		var success:boolean;
		var results:string = 'Test #1: Expect ComputerPlayer label to be \'Computer Player\'';

		var computerPlayer = new TicTacToe.ComputerPlayer();
		if (computerPlayer.label === 'Computer Player') {
			success = true;
			results += ' succeeded.';
		} else {
			success = false;
			results += ' failed.';
		}
		
		displayResults(results, success);
	}

	// Test #2: Expect HumanPlayer label to be 'Human Player'
	export function testTwo() {
		var success:boolean;
		var results:string = 'Test #2: Expect HumanPlayer label to be \'Human Player\'';

		var humanPlayer = new TicTacToe.HumanPlayer();
		if (humanPlayer.label === 'Human Player') {
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