let board = ["","","","","","","","",""];
let cell_ids = ["c1","c2","c3","c4","c5","c6","c7","c8","c9",]
let current_player = "X";

$(document).ready(() => {

  $(".board div").on('click', (event) => {
    selectCell(event.target.id, current_player);
  });

});

function selectCell(elementID, symbol) {
  let idx = parseInt(elementID.replace("c", "")) - 1;
  if (board[idx].length === 0) {
    // if cell is open, place player symbol
    let new_board = board;
    new_board[idx] = symbol;
    board = Object.assign([], new_board);
    current_player = current_player === "X" ? "O" : "X";
    updateBoard();
  } else {
    // else return error message
    console.log("spot taken...");
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
  console.log("board updated...");
}
