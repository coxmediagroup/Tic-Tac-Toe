const GameEngine = {
  board: Array(9).fill(null)
  currentPlayer: "X",
  gameOver: false,
  resetGame: function() {

  },
  toggleCurrentPlayer: function() {

  },
  isValidMove: function(position) {

  },
  checkForVictory: function() {

  },
  makeMove: function(position) {

  }
};

const ViewEngine = {
  refreshBoardView: function(boardState) {

  },
  flashMessage: function(msg) {

  },
  clearFlash: function() {

  }
};

const GameController = {
  onClickNewGame: function(event) {

  },
  onClickBoardSpace: function(event) {

  }
};


window.onload = function() {
  const board = document.querySelectorAll(".board div");
  console.log(board);
}
