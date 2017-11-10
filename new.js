$(document).ready(function(){
  var currentBoard = [];

  var personToken = '';
  var computerToken = '';

  var playerWins = 0;
  var computerWins = 0;
  var ties = 0;

  $('.tile').click(clickTile);

  var winningCombinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 5],[2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]];

  newGame();

  function newGame() {
      $('.selectToken').click(selectToken);
      currentBoard = [1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9];
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
    currentBoard[tileNumber - 1] = currentPlayer;
    $("#" + tileNumber).html(currentPlayer).addClass("played");
    if(checkForWin(currentPlayer, currentBoard)) {
      winGame(currentPlayer);
    };
  };

  function checkForWin(player, gameBoard){
    var gameWon;
    var moves = gameBoard.reduce((array, element, i) =>
      (element === player) ? array.concat(i + 1) : array, []);

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
    console.log(winner);
  };

  function selectBestMove(gameBoard, player) {
    console.log(gameBoard);
    var openTiles = unplayedTiles(gameBoard);

    if (checkForWin(personToken, gameBoard)) {
      return {score: -10};
    } else if (checkForWin(computerToken, gameBoard)) {
      return {score: 10};
    } else if (openTiles.length === 0) {
      return {score: 0};
    }

    var moves = [];
    for (var i = 0; i < openTiles.length; i++) {
      var move = {};
      move.index = gameBoard[openTiles[i]];
      gameBoard[openTiles[i]] = player;
      if (player == computerToken) {
        var result = selectBestMove(gameBoard, personToken);
        move.score = result.score;
      } else {
        var result = selectBestMove(gameBoard, computerToken);
        move.score = result.score;
      }

      gameBoard[openTiles[i]] = move.index;

      moves.push(move);
    }

    var bestMove;
    if(player === computerToken) {
      var bestScore = -10000;
      for(var i = 0; i < moves.length; i++) {
        if (moves[i].score > bestScore) {
          bestScore = moves[i].score;
          bestMove = i;
        }
      }
    } else {
      var bestScore = 10000;
      for(var i = 0; i < moves.length; i++) {
        if (moves[i].score < bestScore) {
          bestScore = moves[i].score;
          bestMove = i;
        }
      }
    }
    return moves[bestMove];
  }
});

