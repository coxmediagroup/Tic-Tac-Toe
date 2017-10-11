// Persistent variables (used for control flow and game state managament)
let board = ["","","","","","","","",""];
let cell_ids = board.map((elem, idx) => { return "c" + idx.toString() });
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

  // Clear the game board (only after next game has been started by selecting symbol)
  cell_ids.forEach((element) => {
    $("#" + element + " i").removeClass();
  })

  // Update game state so that player can interact with the game board
  active_game = !active_game;
  updateMessage("Make your move, Player 1");
}


// Place a symbol in a cell on the game board (used by Player and AI)
function selectCell(idx, symbol) {
  if (board[idx].length === 0) {
    // If cell is open, place symbol
    board[idx] = symbol;

    // Move to the next step in the game loop
    updateBoard();
  } else {
    // else update error message
    updateMessage("That spot is taken, choose another");
  }
}


// Visually update the game board
function updateBoard() {
  for (let i = 0; i < board.length; i++) {
    if (board[i].length > 0) {
      // Get the classes that correspond to the correct symbol for this cell
      let class_set = board[i] === "X" ? "fa fa-fw fa-times" : "fa fa-fw fa-circle-o";

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
  let winCheck = combos.some((c) => {
    return c.every((elem) => {
      return board[elem] === current_player;
    });
  });

  // Check for a draw
  let drawCheck = board.reduce((a,b) => {return a + b}, "").length === 9;

  // Handle endgame conditions or move to the next turn
  if (winCheck || drawCheck) {
    // If it's a win, note who won as a Message and reset the game
    updateMessage(winCheck ? ((current_player === ai_player ? "AI" : "Player 1") + " is the winner") : "It's a draw");
    resetGame();
  } else {
    // If no end conditions are met, let the other player make a move
    current_player = current_player === "X" ? "O" : "X";

    // If the AI is up next, flag that the AI is making a move and the
    if (current_player === ai_player) {
      aiMove();
    }
  }
}

// Helper function that resets game state after win or draw condition has been met
function resetGame() {
  board = ["","","","","","","","",""];
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
    let next_move = nextRandomMove();

    // Update the game state with the move
    selectCell(next_move, ai_player);

    // Turn off the AI move flag and tell Player to make their next move
    ai_move = false;
    updateMessage("Your move, Player 1")
  }, 500);
}

// Helper function to calculate AI move
function nextRandomMove() {
  // Calculate next move using random function
  let x = Math.floor(Math.random() * 8);

  // Verify that their is no existing symbol at that location
  while (board[x].length > 0) {
    // If that location is already taken, recalculate
    x = Math.floor(Math.random() * 8);
  }

  // Return the verified location
  return x;
}
