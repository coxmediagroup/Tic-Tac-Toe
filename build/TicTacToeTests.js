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
    TicTacToeTests.displayResults = displayResults;

    // Test #1: Expect ComputerPlayer label to be 'Computer Player'
    function testOne() {
        var success;
        var results = 'Test #1: Expect ComputerPlayer label to be \'Computer Player\'';

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
    TicTacToeTests.testOne = testOne;

    // Test #2: Expect HumanPlayer label to be 'Human Player'
    function testTwo() {
        var success;
        var results = 'Test #2: Expect HumanPlayer label to be \'Human Player\'';

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
    TicTacToeTests.testTwo = testTwo;
})(TicTacToeTests || (TicTacToeTests = {}));

TicTacToeTests.testOne();
TicTacToeTests.testTwo();
