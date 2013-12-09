var current_move = '';

function addToken(cell) {
    if ( current_move ) { 
        var current_move_cell = document.getElementById(current_move);
        current_move_cell.innerHTML = "";
    }
    cell.innerHTML = "O";
    current_move = cell.id
}
