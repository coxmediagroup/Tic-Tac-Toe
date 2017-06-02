// Basic organization based on an assignment in General Assembly's Web Development Immersive course

const GameEngine = {
  board: Array(9).fill(null),
  currentPlayer: "X",
  gameOver: false,
  resetGame: function() {
    this.board = Array(9).fill(null)
    this.currentPlayer = "X",
      this.gameOver = false;
  },
  toggleCurrentPlayer: function() {
    if (this.currentPlayer == "X") {
      this.currentPlayer = "O";
      this.aiMove();
    } else {
      this.currentPlayer = "X";
    }
  },
  isValidMove: function(position) {
    // A move is valid if the game is not over, the position is in the board, and the position is not occupied
    if (this.gameOver == false) {
      if (this.board.length > position) {
        if (this.board[position] == null) {
          return true;
        }
        return false;
      }
      return false;
    }
    return false;
  },
  checkForVictory: function(board) {
    // Check for column victory
    for (var i = 0; i < 3; i++) {
      if (this.currentPlayer == board[i] && this.currentPlayer == board[i + 3] && this.currentPlayer == board[i + 6]) {
        return true;
      }
    }
    // Check for row victory
    for (var i = 0; i < 3; i += 3) {
      if (this.currentPlayer == board[i] && this.currentPlayer == board[i + 1] && this.currentPlayer == board[i + 2]) {
        return true;
      }
    }
    // Check for diagonal victory
    if (this.currentPlayer == board[0] && this.currentPlayer == board[4] && this.currentPlayer == board[8]) {
      return true;
    }
    if (this.currentPlayer == board[2] && this.currentPlayer == board[4] && this.currentPlayer == board[6]) {
      return true;
    }
    return false;
  },
  makeMove: function(position) {
    if (this.isValidMove(position)) {
      this.board[position] = this.currentPlayer;
      if (this.checkForVictory(this.board)) {
        this.gameOver = true;
      } else {
        this.toggleCurrentPlayer();
      }
      return true;
    }
    ViewEngine.flashMessage("Invalid move, please try again.")
    return false;
  },
  aiMove: function() {
    console.log("Hello");
  }
};

const AI = {
  // Make a 2d array of boards which represent all possible sets of moves
  buildBoard: function() {
    this.board = GameEngine.board;
  },
  // Should output array with scores for each first move
  buildScoreSheet: function() {

  },
  // Outputs array of all possible moves the ai could make
  // check if in this array
  buildPossibleMoves: function() {
    var possibleMoves = [];
    GameEngine.board.forEach(function(piece, pos) {
      if (GameEngine.isValidMove(pos)) {
        possibleMoves.push(pos);
      }
    });
    return possibleMoves;
  },
  // Should iterate over all possible moves and score them
  scoreAllMoves: function() {

  },
  // move is an array index
  // Scores one move
  scoreMove: function(move) {

  },
  // Moves the ai to this position
  makeFakeAIMove: function(move) {

  },
  makeFakeHumanMove: function(move) {

  },
  toggleAIPlayer: function(move) {

  }
}

const ViewEngine = {
  refreshBoardView: function(boardState) {
    var space = document.getElementById("board").firstElementChild;

    for (var i = 0; i < boardState.length; i++) {
      space.innerHTML = boardState[i];
      space = space.nextElementSibling;
    }

    var playerDisplay = document.getElementById("current-player");
    playerDisplay.innerHTML = GameEngine.currentPlayer
  },
  flashMessage: function(msg) {
    var messageBox = document.getElementById("message-box");
    messageBox.innerHTML = msg;
  },
  clearFlash: function() {
    var messageBox = document.getElementById("message-box");
    messageBox.innerHTML = "";
  }
};

const GameController = {
  onClickNewGame: function(event) {
    GameEngine.resetGame();
    ViewEngine.refreshBoardView(GameEngine.board)
    console.log("New game");
  },
  onClickBoardSpace: function(event) {
    var pos = event.path[0].getAttribute("data-position");
    var move = GameEngine.makeMove(pos);
    if (GameEngine.gameOver == true) {
      ViewEngine.flashMessage(`${GameEngine.currentPlayer} has won the game!`)
    }
    ViewEngine.refreshBoardView(GameEngine.board)
  }
};


window.onload = function() {
  // New game click listener
  var button = document.getElementById("new-game");
  button.onclick = GameController.onClickNewGame;
  // Click listeners for spaces
  var space = document.getElementById("board").firstElementChild;
  for (var i = 0; i < 9; i++) {
    space.onclick = GameController.onClickBoardSpace;
    space = space.nextElementSibling;
  }
}
