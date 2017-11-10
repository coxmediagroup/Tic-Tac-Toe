if(!('TicTacToe' in window)) TicTacToe = {};
if(!('Game' in TicTacToe)) TicTacToe.Game = {};
if(!('Player' in TicTacToe)) TicTacToe.Player = {};
if(!('Computer' in TicTacToe)) TicTacToe.Computer = {};

Object.assign(TicTacToe.Game, {
  newGame: function() {

  },
  unplayedtiles: [1, 2, 3, 4, 5, 6, 7, 8, 9],
  winningCombinations: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 5],
                          [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]],
  ties: 0,
  checkForWin: function(moves) {
    this.winningCombinations.forEach(function(combination) {
      var gameWon = combination.every(function(value) {
        return moves.indexOf(value) !== -1;
      });
      if (gameWon) {
        winGame(moves);
      };
    });
  },
  winGame: function(moves) {
    var player = TicTacToe.Player;
    var computer = TicTacToe.Computer;
    if (moves === player.moves) {
      player.wins++;
      $('#playerScore').html(player.wins);
      $("#winModal").modal()
      return
      } else if (moves === computer.moves) {
        computer.wins++;
        alert('You lost');
        $("#loseGame").modal()
      }
  },
  checkForTie() {
    if (this.unplayedTiles.length == 0) {
      TicTacToe.Game.ties++;
      alert('You Tied');
      $("#tieGame").modal();
    }
  }
});

Object.assign(TicTacToe.Player, {
  token: '',
  moves: [],
  wins: 0,
  selectToken: function(event) {
    var computer = TicTacToe.Computer;
    this.token = event.target.dataset.id;
    $('.chooseToken').addClass('hide');
    this.token === 'X' ? computer.token = 'O' : computer.token = 'X';
  },
  makeMove: function(event) {
    if (event.target.classList.contains('played')) {
      alert("Square already played")
    } else if ( this.token === '' ) {
      alert('select X or O');
      } else {
          var unplayed = TicTacToe.Game.unplayedTiles;
          var tile = event.target
          tile.innerHTML = this.token;
          tile.classList.add("played", this.token);
          this.moves.push(parseInt(tile.dataset.id));
          unplayed.splice(unplayed.indexOf(parseInt(tile.dataset.id)), 1);
          checkForWin(this.moves);
          checkForTie();
          setTimeout(computerMove, 2000);
        };
  }
});

Object.assign(TicTacToe.Computer, {
  token: '',
  moves: [],
  wins: 0,
  makeMove: function(){
    var unplayed = TicTacToe.Game.unplayedTiles;
    var tileNumber = unplayed[Math.floor(Math.random() *
                                    unplayed.length)]
    var tile = $('[data-id = ' + tileNumber.toString() + ']');
    tile.addClass("played").html(this.token);
    this.moves.push(tileNumber);
    unplayed.splice(unplayed.indexOf(tileNumber), 1);
    checkForWin(this.moves);
    checkForTie();
  },

});

