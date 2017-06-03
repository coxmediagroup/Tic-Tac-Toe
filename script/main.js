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
      AI.makeMove();
    } else {
      this.currentPlayer = "X";
    }
  },
  isValidMove: function(position) {
    // A move is valid if the game is not over, the position is in the board, and the position is not occupied
    if (this.gameOver == false) {
      if (position < GameEngine.board.length) {
        if (GameEngine.board[position] == null) {
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
    for (var i = 0; i < 9; i += 3) {
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
  checkForTie: function(board) {
    for (var i = 0; i < board.length; i++) {
      if (board[i] == null) {
        return false;
      }
    }
    if (GameEngine.checkForVictory(board)) {
      return false;
    } else {
      return true;
    }
  },
  makeMove: function(position) {
    if (this.isValidMove(position)) {
      this.board[position] = this.currentPlayer;
      if (this.checkForVictory(this.board) || this.checkForTie(this.board)) {
        this.gameOver = true;
      } else {
        this.toggleCurrentPlayer();
      }
      return true;
    }
    ViewEngine.flashMessage("Invalid move, please try again.")
    return false;
  }
};

const AI = {
  makeMove: function() {
    var possibleMoves = this.buildPossibleMoves(GameEngine.board);
    var lossPosition = this.findLoss(possibleMoves);
    var winPosition = this.findVictory(possibleMoves);

    if (winPosition != false) {
      GameEngine.makeMove(winPosition);
    } else if (lossPosition != false) {
      GameEngine.makeMove(lossPosition);
    } else {
      var max = Math.floor(possibleMoves.length);
      var i = Math.floor(Math.random() * max);
      GameEngine.makeMove(possibleMoves[i]);
      ViewEngine.refreshBoardView(GameEngine.board);
      ViewEngine.clearFlash();
    }
  },
  checkForVictory: function(board, player) {
    // Check for column victory
    for (var i = 0; i < 3; i++) {
      if (player == board[i] && player == board[i + 3] && player == board[i + 6]) {
        return true;
      }
    }
    // Check for row victory
    for (var i = 0; i < 9; i += 3) {
      if (player == board[i] && player == board[i + 1] && player == board[i + 2]) {
        return true;
      }
    }
    // Check for diagonal victory
    if (player == board[0] && player == board[4] && player == board[8]) {
      return true;
    }
    if (player == board[2] && player == board[4] && player == board[6]) {
      return true;
    }
    return false;
  },
  // Outputs array of all possible moves the ai could make
  buildPossibleMoves: function(board) {
    var possibleMoves = [];
    board.forEach(function(piece, pos) {
      if (GameEngine.isValidMove(pos)) {
        possibleMoves.push(pos);
      }
    });
    return possibleMoves;
  },
  // Moves the ai to this position, returns temp board
  makeFakeAIMove: function(move) {
    var board = [];
    board.push(GameEngine.board);
    board[move] = "O";
    return board;
  },
  makeFakeHumanMove: function(move) {
    var board = [];
    GameEngine.board.forEach(function(el) {
      board.push(el);
    })
    board[move] = "X";
    return board;
  },
  findVictory: function(possibleMoves) {
    var board;
    for (var i = 0; i < possibleMoves.length; i++) {
      board = AI.makeFakeAIMove(i);
      if (AI.checkForVictory(board, "O")) {
        return i;
      }
    }
    return false;
  },
  findLoss: function(possibleMoves) {
    var board;
    for (var i = 0; i < possibleMoves.length; i++) {
      board = AI.makeFakeHumanMove(i);
      if (AI.checkForVictory(board, "X")) {
        return i;
      }
    }
    return false;
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
    ViewEngine.refreshBoardView(GameEngine.board);
    ViewEngine.clearFlash();
  },
  onClickBoardSpace: function(event) {
    var pos = event.path[0].getAttribute("data-position");
    var move = GameEngine.makeMove(pos);
    if (GameEngine.gameOver == true) {
      if (GameEngine.checkForTie(GameEngine.board) == true) {
        ViewEngine.flashMessage("It's a tie!")
      } else {
        ViewEngine.flashMessage(`${GameEngine.currentPlayer} has won the game!`)
      }
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
