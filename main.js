let board = ["","","","","","","","",""];
let cell_ids = ["c1","c2","c3","c4","c5","c6","c7","c8","c9",]
let current_player = "X";
let ai_player = "";
let active_game = false;
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

$(document).ready(() => {

  $("#x_select, #o_select").on('click', (event) => {
    if (!active_game) {
      selectSymbol(event.currentTarget.id.replace("_select", "").toUpperCase());
    }
  });

  $(".board div").on('click', (event) => {
    if (active_game) {
      selectCell((parseInt(event.target.id.replace("c", "")) - 1), current_player);
    } else {
      updateMessage("Select your symbol");
    }
  });

});

function selectSymbol(symbol) {
  ai_player = symbol === "X" ? "O" : "X";
  cell_ids.forEach((element) => {
    $("#" + element + " i").removeClass();
  })
  active_game = !active_game;
  if (symbol !== current_player) {
    // Start AI turn
    updateMessage("AI is thinking");
    aiMove();
  } else {
    updateMessage("Make your move, Player 1");
  }
}

function selectCell(idx, symbol) {
  if (board[idx].length === 0) {
    // if cell is open, place player symbol
    let new_board = board;
    new_board[idx] = symbol;
    board = Object.assign([], new_board);
    updateBoard();
  } else {
    // else return error message
    updateMessage("spot taken...");
  }
}

function updateBoard() {
  for (let i = 0; i < board.length; i++) {
    if (board[i].length > 0) {
      let class_set = board[i] === "X" ? "fa fa-fw fa-times" : "fa fa-fw fa-circle-o";
      $("#" + cell_ids[i] + " i").removeClass();
      $("#" + cell_ids[i] + " i").addClass(class_set);
    }
  }
  updateMessage("board updated...");
  endCheck();
}

function updateMessage(m) {
  $(".game_message").text(m);
}

function endCheck() {
  // Check for any wins
  let winCheck = combos.some((c) => {
    return c.every((elem) => {
      return board[elem] === current_player;
    });
  });

  console.log(current_player);
  console.log(ai_player);

  // Check for a draw
  let drawCheck = board.reduce((a,b) => {return a + b}, "").length === 9;
  // Handle endgame conditions or move to the next turn
  if (winCheck) {
    updateMessage((current_player === ai_player ? "AI" : "Player 1") + " is the winner");
    resetGame();
  } else if (drawCheck) {
    updateMessage("It's a draw");
    resetGame();
  } else {
    current_player = current_player === "X" ? "O" : "X";
    if (current_player === ai_player) {
      aiMove();
    }
  }
}

function resetGame() {
  board = ["","","","","","","","",""];
  current_player = "X";
  ai_player = "";
  active_game = !active_game;
  // cell_ids.forEach((element) => {
  //   $("#" + element + " i").removeClass();
  // })
}

function aiMove() {
  setTimeout(() => {
    let x = Math.floor(Math.random() * 8);
    while (board[x].length > 0) {
      x = Math.floor(Math.random() * 8);
    }
    selectCell(x, ai_player);
  }, 1500)
}
