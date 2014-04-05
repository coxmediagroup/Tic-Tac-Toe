/// <reference path="TicTacToe.ts" />
/// <reference path="ComputerPlayer.ts" />
/// <reference path="HumanPlayer.ts" />
var TicTacToeTests;
(function (TicTacToeTests) {
    function displayResults(results, success) {
        var color;
        (success) ? color = 'green' : color = 'red';
        var p = document.createElement("p");
        p.style.color = color;
        p.innerHTML = results;
        document.getElementById("testResults").appendChild(p);
    }

    // Test #1: Expect ComputerPlayer label to be 'Computer Player'.
    function testOne() {
        var success;
        var results = 'Test #1: Expect ComputerPlayer label to be \'Computer Player\'';

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
    TicTacToeTests.testOne = testOne;

    // Test #2: Expect HumanPlayer label to be 'Human Player'.
    function testTwo() {
        var success;
        var results = 'Test #2: Expect HumanPlayer label to be \'Human Player\'';

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
    TicTacToeTests.testTwo = testTwo;

    // Test #3: Expect both players' initial score to be 0.
    function testThree() {
        var success;
        var results = 'Test #3: Expect both players\' initial score to be 0';

        var humanPlayer = new TicTacToe.HumanPlayer();
        var computerPlayer = new TicTacToe.ComputerPlayer();

        console.log('Human Player Score: ' + humanPlayer.getScore());
        console.log('Computer Player Score: ' + computerPlayer.getScore());

        if (humanPlayer.getScore() === 0 && computerPlayer.getScore() === 0) {
            success = true;
            results += ' succeeded.';
        } else {
            success = false;
            results += ' failed.';
        }

        displayResults(results, success);
    }
    TicTacToeTests.testThree = testThree;
})(TicTacToeTests || (TicTacToeTests = {}));

TicTacToeTests.testOne();
TicTacToeTests.testTwo();
TicTacToeTests.testThree();
