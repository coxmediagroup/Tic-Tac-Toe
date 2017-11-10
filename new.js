$(document).ready(function(){
  var currentBoard = [];

  var personToken = '';
  var computerToken = '';

  var playerWins = 0;
  var computerWins = 0;
  var ties = 0;

  $('.tile').click(clickTile);

  var winningCombinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],[1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];

  newGame();

  function newGame() {
      $('.selectToken').click(selectToken);
      $('.playAgain').click(newGame);
      currentBoard = [0, 1, 2, 3, 4, 5, 6, 7, 8];
      $('.tile').html('').removeClass('played');
      $('#selectTokenModal').modal('show');
  };

  function selectToken(event) {
    personToken = event.target.dataset.id;
    $('.chooseToken').addClass('hide');
    personToken === 'X' ? computerToken = 'O' : computerToken = 'X';
  };

  function clickTile(event){
    if (event.target.classList.contains('played')) {
      alert("Square already played")
    } else {
      makeMove(personToken, event.target.id);
      if(!checkForWin(personToken, currentBoard) && !checkForTie()){
        makeMove(computerToken, computerMove());
      }
    }
  };

  function makeMove(currentPlayer, tileNumber){
    currentBoard[tileNumber] = currentPlayer;
    $("#" + tileNumber).html(currentPlayer).addClass("played");
    if(checkForWin(currentPlayer, currentBoard)) {
      winGame(currentPlayer);
    };
  };

  function checkForWin(player, gameBoard){
    var gameWon;
    var moves = gameBoard.reduce((array, element, i) =>
      (element === player) ? array.concat(i) : array, []);

    winningCombinations.forEach(function(combination) {
      var threeInARow = combination.every(function(value) {
        return moves.indexOf(value) !== -1;
      });
      if (threeInARow) gameWon = true;
    });
    return gameWon;
  };

  function checkForTie(){
    if( unplayedTiles(currentBoard).length === 0 ) {
      ties++;
      $("#tieGame").modal();
      $('#tieScore').html(ties);
      return true;
    }
    else return false;
  };

  function unplayedTiles(gameBoard) {
    return gameBoard.filter(element => typeof element == 'number');
  };

  function computerMove() {
    return selectBestMove(currentBoard, computerToken).index;
  };

  function winGame(winner) {
    if (winner === personToken) {
      personWins++;
      $('#playerScore').html(playerWins);
      $("#winModal").modal();
    } else {
      computerWins++;
      $('#computerScore').html(computerWins);
      $("#loseGame").modal()
    }
  };

  function selectBestMove(gameBoard, player) {
    var openTiles = unplayedTiles(gameBoard);

    if (checkForWin(personToken, gameBoard)) {
      return {score: -10};
    } else if (checkForWin(computerToken, gameBoard)) {
      return {score: 10};
    } else if (openTiles.length === 0) {
      return {score: 0};
    }

    var moves = [];
    openTiles.forEach(function(tile, i) {
      var move = {};
      move.index = gameBoard[tile];
      gameBoard[tile] = player;
      if (player == computerToken) {
        var result = selectBestMove(gameBoard, personToken);
        move.score = result.score;
      } else {
        var result = selectBestMove(gameBoard, computerToken);
        move.score = result.score;
      }
      gameBoard[tile] = move.index;
      moves.push(move);
    });

    var bestMove;
    if(player === computerToken) {
      var bestScore = -10000;
      moves.forEach(function(move, i) {
        if (move.score > bestScore) {
          bestScore = move.score;
          bestMove = i;
        }
      });
    } else {
      var bestScore = 10000;
      // for(var i = 0; i < moves.length; i++) {
        moves.forEach(function(move, i) {
        if (move.score < bestScore) {
          bestScore = move.score;
          bestMove = i;
        }
      });
    }
    return moves[bestMove];
  }
});

