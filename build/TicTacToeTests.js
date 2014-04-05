/// <reference path="Game.ts" />
/// <reference path="Player.ts" />
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

    // Test #4: If computer player has two in a row, expect computer player to play the third to get three in a row and win the game.
    function testFour() {
        var success;
        var results = 'Test #4: If computer player has two in a row, expect computer player to play the third to get three in a row and win the game';

        var game = new TicTacToe.Game();
        var humanPlayer = new TicTacToe.HumanPlayer();
        var computerPlayer = new TicTacToe.ComputerPlayer();

        humanPlayer.registerObserver(game);
        humanPlayer.registerObserver(computerPlayer);
        computerPlayer.registerObserver(game);

        computerPlayer.makeMove(0);
        humanPlayer.makeMove(1);
        computerPlayer.makeMove(3);
        humanPlayer.makeMove(7);
        var moveIndex = computerPlayer.makeMove();

        if (moveIndex === 6 && game.getWinner() && game.getWinner() === computerPlayer.getLabel()) {
            success = true;
            results += ' succeeded.';
        } else {
            success = false;
            results += ' failed.';
        }

        displayResults(results, success);
    }
    TicTacToeTests.testFour = testFour;

    // Test #5: If human player has two in a row, expect computer player to play the third to block human player and win the game.
    function testFive() {
        var success;
        var results = 'Test #5: If human player has two in a row, expect computer player to play the third to block human player and win the game';
        var game = new TicTacToe.Game();
        var humanPlayer = new TicTacToe.HumanPlayer();
        var computerPlayer = new TicTacToe.ComputerPlayer();

        humanPlayer.registerObserver(game);
        humanPlayer.registerObserver(computerPlayer);
        computerPlayer.registerObserver(game);

        humanPlayer.makeMove(0);
        computerPlayer.makeMove(1);
        humanPlayer.makeMove(3);

        var moveIndex = computerPlayer.makeMove();
        humanPlayer.makeMove(2);
        computerPlayer.makeMove(7);
        humanPlayer.makeMove(5);
        var moveIndex2 = computerPlayer.makeMove();

        var winner = game.getWinner();

        if (moveIndex === 6 && moveIndex2 === 8 && winner && winner === computerPlayer.getLabel()) {
            success = true;
            results += ' succeeded.';
        } else {
            success = false;
            results += ' failed.';
        }

        displayResults(results, success);
    }
    TicTacToeTests.testFive = testFive;

    // Test #6: Expect computer player to create a forking opportunity where computer player can win in two ways and win the game.
    function testSix() {
        var success;
        var results = 'Test #6: Expect computer player to create a forking opportunity where computer player can win in two ways and win the game';
        var game = new TicTacToe.Game();
        var humanPlayer = new TicTacToe.HumanPlayer();
        var computerPlayer = new TicTacToe.ComputerPlayer();

        humanPlayer.registerObserver(game);
        humanPlayer.registerObserver(computerPlayer);
        computerPlayer.registerObserver(game);

        computerPlayer.makeMove(4);
        humanPlayer.makeMove(7);
        computerPlayer.makeMove(8);
        humanPlayer.makeMove(0); // blocks computer's first chance at winning
        var moveIndex = computerPlayer.makeMove();
        humanPlayer.makeMove(3);
        var moveIndex2 = computerPlayer.makeMove();

        var winner = game.getWinner();

        if (moveIndex === 5 && moveIndex2 === 2 && winner && winner === computerPlayer.getLabel()) {
            success = true;
            results += ' succeeded.';
        } else {
            success = false;
            results += ' failed.';
        }

        displayResults(results, success);
    }
    TicTacToeTests.testSix = testSix;
})(TicTacToeTests || (TicTacToeTests = {}));

TicTacToeTests.testOne();
TicTacToeTests.testTwo();
TicTacToeTests.testThree();
TicTacToeTests.testFour();
TicTacToeTests.testFive();
TicTacToeTests.testSix();
