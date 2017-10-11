// Persistent variables (used for control flow and game state managament)
let current_board = ["","","","","","","","",""];
let cell_ids = current_board.map((elem, idx) => { return "c" + idx.toString() });
let current_player = "";
let ai_player = "";
let ai_move = false;
let active_game = false;
// Potential winning combinations of moves
let combos = [
  [0,1,2],
  [3,4,5],
  [6,7,8],
  [0,3,6],
  [1,4,7],
  [2,5,8],
  [0,4,8],
  [2,4,6]
];


// DOM Event Handling
$(document).ready(() => {
  // Select symbol to begin a game
  $("#x_select, #o_select").on('click', (event) => {
    if (!active_game) {
      selectSymbol(event.currentTarget.id.replace("_select", "").toUpperCase());
    }
  });

  // Select a move, or wait for AI to make its move
  $(".board div").on('click', (event) => {
    if (active_game && !ai_move) {
      // If the symbols have been selected and AI is not currently moving, Player's move is accepted as valid input
      selectCell(parseInt(event.target.id.replace("c", "")), current_player);
    } else if (ai_move) {
      // If the AI is moving, Player is told to wait, otherwise Player must choose symbol to start the game
      updateMessage(ai_move ? "Wait for the AI to make its move" : "Select symbol to start game")
    }
  });
});


// Select your symbol (Used at the start of each game)
function selectSymbol(symbol) {
  // Player moves first, and AI takes the other symbol
  current_player = symbol;
  ai_player = symbol === "X" ? "O" : "X";

  // Clear the game current_board (only after next game has been started by selecting symbol)
  cell_ids.forEach((element) => {
    $("#" + element + " i").removeClass();
  })

  // Update game state so that player can interact with the game current_board
  active_game = !active_game;
  updateMessage("Make your move, Player 1");
}


// Place a symbol in a cell on the game current_board (used by Player and AI)
function selectCell(idx, symbol) {
  if (current_board[idx].length === 0) {
    // If cell is open, place symbol
    current_board[idx] = symbol;

    // Move to the next step in the game loop
    updateBoard();
  } else {
    // else update error message
    updateMessage("That spot is taken, choose another");
  }
}


// Visually update the game current_board
function updateBoard() {
  for (let i = 0; i < current_board.length; i++) {
    if (current_board[i].length > 0) {
      // Get the classes that correspond to the correct symbol for this cell
      let class_set = current_board[i] === "X" ? "fa fa-fw fa-times" : "fa fa-fw fa-circle-o";

      // Remove previous classes and add new classes
      $("#" + cell_ids[i] + " i").removeClass();
      $("#" + cell_ids[i] + " i").addClass(class_set);
    }
  }

  // Move to the next step in the game loop
  endCheck();
}


// Simple helper function that updates Message area in game with current status
function updateMessage(m) {
  $(".game_message").text(m);
}


// Check for game-ending conditions (win or draw), otherwise trigger the next move
// If last move was the Player, trigger a move by the AI
function endCheck() {
  // Check for a win for the current player
  let win_check = winCheck(current_board);

  // Check for a draw
  let draw_check = drawCheck(current_board);

  // Handle endgame conditions or move to the next turn
  if (win_check || draw_check) {
    // If it's a win, note who won as a Message and reset the game
    updateMessage(win_check ? ((current_player === ai_player ? "AI" : "Player 1") + " is the winner. Select your symbol to start a new game.") : "It's a draw. Select your symbol to start a new game.");
    resetGame();
  } else {
    // If no end conditions are met, let the other player make a move
    current_player = current_player === "X" ? "O" : "X";

    // If the AI is up next, flag that the AI is making a move and the
    if (current_player === ai_player) {
      aiMove();
    } else {
      updateMessage("Your move, Player 1")
    }
  }
}

// Helper function for determining if the game is won
function winCheck(board) {
  return combos.some((c) => {
    return c.every((elem) => { return board[elem] === "X"; }) || c.every((elem) => { return board[elem] === "O"; });
  });
}

// Helper function for determining if the game is a draw
function drawCheck(board) {
  return board.reduce((a,b) => {return a + b}, "").length === 9;
}

// Helper function that resets game state after win or draw condition has been met
function resetGame() {
  current_board = ["","","","","","","","",""];
  current_player = "";
  ai_player = "";
  active_game = !active_game;
}

// Helper function to process AI move calculation
function aiMove() {
  // Flag AI move in progress so that Player input is not accepted
  ai_move = true;

  // Update message so that Player knows what's happening
  updateMessage("AI is thinking");

  // setTimeout creates the illusion that AI is "thinking"
  setTimeout(() => {

    // Select the location for the next move
    let next_move = nextBestMove();

    // Update the game state with the move
    selectCell(next_move, ai_player);

    // Turn off the AI move flag and tell Player to make their next move
    ai_move = false;
  }, 500);
}

// Helper function to calculate AI move
function nextRandomMove() {
  // Get all open moves from helper function
  let potential_moves = getPotentialMoves(current_board);

  // Calculate next move using random function
  let x = potential_moves[Math.floor(Math.random() * potential_moves.length)];

  // Return the verified location
  return x;
}

// Function for determining the best move
function nextBestMove() {
  var best_move = -1;
  var best_move_score = 0;

  // Grab the set of potential moves
  var potential_moves = getPotentialMoves(current_board);

  potential_moves.forEach((move) => {
    // Make each move on a copy of the board
    var board = Object.assign([], current_board);
    board[move] = ai_player;

    // Get the score for each move
    var move_score = getMoveScore(0, false, board);

    // If this move has a better score, save it as the best move
    if (move_score > best_move_score || best_move === -1) {
      best_move = move;
      best_move_score = move_score;
    }
  });

  // Return the best move for the AI to use
  return best_move;
}

// Recursive function that determines the score of each potential move
function getMoveScore(depth, is_maximizer, board) {
  //Check to see if the game is over (win/draw). If so, send the score back up the recursive tree.
  if (winCheck(board)) {
    return is_maximizer ? (-10 + depth) : (10 - depth);
  } else if (drawCheck(board)) {
    return 0;
  }

  // Grab the next set of potential moves
  var potential_moves = getPotentialMoves(board);
  var best_move_score;

  // If the last theoretical move was made by the AI, then project the best move for Player (and vice versa)
  // Uses the same form of comparison as the original nextBestMove() function
  if (is_maximizer) {
    best_move_score = -10;
    potential_moves.forEach((move) => {
      var potential_board = Object.assign([], board);
      potential_board[move] = ai_player;
      var potential_score = getMoveScore(depth + 1, !is_maximizer, potential_board);
      potential_board[move] = "";
      best_move_score = best_move_score > potential_score ? best_move_score : potential_score;
    });
  } else {
    best_move_score = 10;
    potential_moves.forEach((move) => {
      var potential_board = Object.assign([], board);
      potential_board[move] = ai_player === "X" ? "O" : "X";
      var potential_score = getMoveScore(depth + 1, !is_maximizer, potential_board);
      potential_board[move] = "";
      best_move_score = best_move_score < potential_score ? best_move_score : potential_score;
    });
  }

  // Return the the best move score for comparison purposes in the parent function
  return best_move_score;
}

// Helper function to grab the potential moves from the current board and return them as indices for easy comparison
function getPotentialMoves(board) {
  return board.map((elem, idx) => {
    return elem.length === 0 ? idx : -1;
  }).filter((elem) => {
    return elem >= 0;
  });
}
