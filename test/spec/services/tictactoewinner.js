'use strict';

describe('Service: TicTacToeWinner', function () {

  // load the service's module
  beforeEach(module('ticTacToeApp'));

  // instantiate service
  var TicTacToeWinner;
  var Gameboard;
  beforeEach(inject(function (_TicTacToeWinner_) {
    TicTacToeWinner = _TicTacToeWinner_;
  }));

  beforeEach(inject(function (_Gameboard_) {
    Gameboard = _Gameboard_;
  }));

  it('should suggest a move to block a row 1 win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X

    expect(TicTacToeWinner.defend('O')).toBe('C1');
  });


  it('should suggest a move to block a row 2 win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('A2'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B2'); // O
    expect(TicTacToeWinner.defend('X')).toBe('C2');

  });

  it('should suggest a move to block a row 3 win', function () {
    Gameboard.play('A2'); // X
    Gameboard.play('A3'); // O
    Gameboard.play('B1'); // X
    Gameboard.play('B3'); // O
    expect(TicTacToeWinner.defend('X')).toBe('C3');
  });

  it('should suggest a move to block a col A win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('A2'); // X
    expect(TicTacToeWinner.defend('O')).toBe('A3');

  });

  it('should suggest a move to block a col B win', function () {
    Gameboard.play('B1'); // X
    Gameboard.play('C3'); // O
    Gameboard.play('B2'); // X

    expect(TicTacToeWinner.defend('O')).toBe('B3');
  });

  it('should suggest a move to block a col C win', function () {
    Gameboard.play('C1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('C2'); // X
    expect(TicTacToeWinner.defend('O')).toBe('C3');

  });


  it('should suggest a move to block a diagonal (from top left) win', function () {
    Gameboard.play('A1'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    expect(TicTacToeWinner.defend('O')).toBe('C3');
  });

  it('should suggest a move to block a diagonal (from top right) win', function () {
    Gameboard.play('A3'); // X
    Gameboard.play('B3'); // O
    Gameboard.play('B2'); // X
    expect(TicTacToeWinner.defend('O')).toBe('C1');
  });

  it('should see chances to win in the next move', function() {
    Gameboard.play('B2');// X
    Gameboard.play('C2');// O
    Gameboard.play('B1');// X
    expect(TicTacToeWinner.winningMove('X')).toBe('B3');
  });

  it('should see chances to take an opposite corner', function() {
    Gameboard.play('A1');// X
    expect(TicTacToeWinner.takeAnOppositeCorner('O')).toBe('C3');

  });

  it('should see chances to fork (2 ways to win)', function() {
    Gameboard.play('A3');// X
    Gameboard.play('C2');// O
    Gameboard.play('B1');// X
    Gameboard.play('C3');// O

    var fork = TicTacToeWinner.forkOpponent('X');
    expect(fork === 'C1' || fork === 'A1').toBe(true);
  });



  it('should see chances to take the center', function() {
    expect(TicTacToeWinner.takeCenterIfWeCan()).toBe('B2');
    Gameboard.play('B2');// X
    expect(TicTacToeWinner.takeCenterIfWeCan()).toBe('');

  });

  it('should take corners if empty', function() {
    Gameboard.play('A3');// X
    Gameboard.play('A1');// O
    Gameboard.play('C1');// X
    expect(TicTacToeWinner.takeAnyCorner()).toBe('C3');
  });

  it('should take sides if empty', function() {
    Gameboard.play('A2');// X
    Gameboard.play('B1');// O
    Gameboard.play('B3');// X
    expect(TicTacToeWinner.takeAnySide()).toBe('C2');

  });
//Human:A1, CPU:B3, Human:C2

  it('should block the opponent fork (2 ways to win), by going on the offensive', function() {
    Gameboard.play('A3');// X
    Gameboard.play('C2');// O
    Gameboard.play('B1');// X

    var forkBlock = TicTacToeWinner.blockFork('O');
    Gameboard.play(forkBlock); // O

    expect(TicTacToeWinner.defend('X')).not.toBe('');
  });


  it('should always win against randomized X opponent', function () {
    var wins = 0;

    for (var i = 0; i < 50; i++) {
      var humanMoves = ['A1', 'B3', 'C2', 'C1', 'B2', 'A3', 'C3', 'A2', 'B1'];

      for (var j = 0; j < humanMoves.length; j++) {
        var other = Math.floor(Math.random() * humanMoves.length);
        if (other === j) continue;
        var tmp = humanMoves[j];
        humanMoves[j] = humanMoves[other];
        humanMoves[other] = tmp;
      }


      while(humanMoves.length > 0) {
        // let player go first (X)

        var move;
        while (humanMoves.length > 0) {
          move = humanMoves.shift();
          if (Gameboard[move] === '') {
            break;
          }
          move = '';
        }

        if (move) {
          Gameboard.play(move);
          if (Gameboard.winner()) break;
        }

        var compMove = TicTacToeWinner.suggestMoveFor('O');
        Gameboard.play(compMove);
        

        if (Gameboard.winner() !== '') break;

      }
      if (Gameboard.winner() === 'O') {
        wins++;
      }

      Gameboard.reset();
    }

    expect(wins > 40).toBe(true);

  });

  it('should always win against randomized O opponent', function () {
    var wins = 0;
    for (var i = 0; i < 50; i++) {
      var humanMoves = ['A1', 'B3', 'C2', 'C1', 'B2', 'A3', 'C3', 'A2', 'B1'];

      // shuffle moves
      for (var j = 0; j < humanMoves.length; j++) {
        var other = Math.floor(Math.random() * humanMoves.length);
        if (other === j) continue;
        var tmp = humanMoves[j];
        humanMoves[j] = humanMoves[other];
        humanMoves[other] = tmp;
      }


      while(humanMoves.length > 0) {
        // let player go first (X)
        Gameboard.play(TicTacToeWinner.suggestMoveFor('X'));

        if (Gameboard.winner() !== '') {
          break;
        }

        var move;
        while (humanMoves.length > 0) {
          move = humanMoves.shift();
          if (Gameboard[move] === '') {
            break;
          }
          move = '';
        }

        if (move) {
          Gameboard.play(move);
          if (Gameboard.winner()) break;
        }

      }

      if (Gameboard.winner() === 'X') wins++;

      Gameboard.reset();
    }

    expect(wins > 40).toBe(true);
  });
});
