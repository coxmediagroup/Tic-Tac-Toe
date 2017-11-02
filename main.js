$(document).ready(function(){
    var playerToken = '';
    var computerToken = '';
    var playerMoves = [];
    var computerMoves = [];
    var playerWins = 0;
    var computerWins = 0;
    var ties = 0;
    var unplayedTiles = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    var winningCombinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 5],
                               [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]];

  $('.selectToken').click(selectToken);
  $('.playAgain').click(newGame);
  $('.tile').click(playerMove);
  $('#selectTokenModal').modal('show');
  $('#computerScore').html(computerWins);
  $('#tieScore').html(ties)

  function selectToken(event) {
    playerToken = event.target.dataset.id;
    $('.chooseToken').addClass('hide');
    playerToken === 'X' ? computerToken = 'O' : computerToken = 'X';
  };

  function playerMove(event) {
    if (event.target.classList.contains('played')) {
      alert("Square already played")
    } else if ( playerToken === '' ) {
      alert('select X or O');
      } else {
          var tile = event.target
          tile.innerHTML = playerToken;
          tile.classList.add("played", playerToken);
          playerMoves.push(parseInt(tile.dataset.id));
          unplayedTiles.splice(unplayedTiles.indexOf(parseInt(tile.dataset.id)), 1);
          checkForWin(playerMoves);
          checkForTie();
          setTimeout(computerMove, 2000);
        };
  };

  function computerMove(){
    console.log(unplayedTiles);
    var tileNumber = unplayedTiles[Math.floor(Math.random() * unplayedTiles.length)]
    var tile = $('[data-id = ' + tileNumber.toString() + ']');
    tile.addClass("played").html(computerToken);
    computerMoves.push(tileNumber);
    unplayedTiles.splice(unplayedTiles.indexOf(tileNumber), 1);
    checkForWin(computerMoves);
    checkForTie();

  };

  function checkForWin(moves){
    winningCombinations.forEach(function(combination) {
      var gameWon = combination.every(function(value) {
        return moves.indexOf(value) !== -1;
      });
      if (gameWon) {
        winGame(moves);
      };
    });
  };
  function winGame(moves){
    if (moves === playerMoves) {
      playerWins++;
      $('#playerScore').html(playerWins);
      $("#winModal").modal()
      return
    } else if (moves === computerMoves) {
      computerWins++;
      $('#computerScore').html(computerWins);
      $("#loseGame").modal()
    }
  };
  function checkForTie(){
    if (unplayedTiles.length == 0) {
      ties++;
      $("#tieGame").modal();
      $('#tieScore').html(ties);
    }
  };
  function newGame() {
    playerToken = '';
    computerToken = '';
    playerMoves = [];
    computerMoves = [];
    unplayedTiles = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    winningCombinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 5],
                               [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]];
    $('.tile').html('').removeClass('played');
    $('#selectTokenModal').modal('show');
  }
});
