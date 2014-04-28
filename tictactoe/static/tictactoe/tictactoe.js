/**
 * Get a jQuery object for a specific cell.
 */
function getCellElem(row, col) {
    return $("#board-cell-" + row + "-" + col);
}

/**
 * Get a string representing the state of the game board at row, col.
 *
 * See getCellStrForElem() for info about the return type.
 */
function getCellStr(row, col) {
    var cellElem = getCellElem(row, col);
    return getCellStrForElem(cellElem.get())
}

/**
 * Get a string for the cell represented by the given DOM element.
 *
 * Returns ' ' for an empty cell, 'X' for a cell taken by X, and 'O' for a
 * cell taken by O.
 */
function getCellStrForElem(elem) {
    var content = $(elem).text();

    // empty cells are represented with a space char
    if(!content.trim()) {
        content = ' ';
    }

    return content;
}


/**
 * Get a list of strings representing the current board.
 */
function getBoard() {
    var board = []
    for(var row = 0; row < 3; row++) {
        var rowStr = ''
        for(var col = 0; col < 3; col++) {
            var content = getCellStr(row, col);
            rowStr += content;
        }
        board.push(rowStr);
    }
    return board;
}


/**
 * Mark the cell at row, col for the player, if possible.
 *
 * Returns true if it succeeded, and false if it failed (i.e. the cell
 * has already been taken).
 */
function tryTakeCell(cellElem) {
    var cell = getCellStrForElem(cellElem);
    if(cell != ' ') {
        return false;
    } else {
        $(cellElem).text('X');
        return true;
    }
}


/**
 * Set the DOM to reflect the given board.
 *
 * boardModel is a list of 3 strings, all themselves having length 3.
 * Each string is a row of the game board. Each character is either ' ', if
 * the cell at that position is empty, 'X' if the X player has taken the cell,
 * or 'O' of the O player has taken the cell.
 */
function updateBoard(boardModel) {
    for(var row = 0; row < 3; row++) {
        for(var col = 0; col < 3; col++) {
            var content = boardModel[row][col];
            var cellElem = getCellElem(row, col);
            cellElem.text(content);
        }
    }
}


/**
 * Update the page based on the server's response.
 *
 * The response includes the new game state as well as the AI's move.
 */
function handleResponse(response) {
    updateBoard(response.board);
    var state = response['state'];
    if(state == "DRAW") {
        $(".game-state-output").text("Draw!");
    } else if(state == "VICTORY") {
        $(".game-state-output").text("The computer wins!");
        response.cells.forEach(function(cell) {
            var row = cell[0];
            var col = cell[1];
            getCellElem(row, col).addClass("win-cell");
        });
    }
}


$(document).ready(function() {

    $("#tictactoe-board td").click(function() {
        var isLegalMove = tryTakeCell(this);
        if(isLegalMove) {
            var boardData = JSON.stringify(getBoard());
            $.ajax({
                url: window.AI_URL,
                type: "POST",
                data: boardData,
                contentType: 'application/json; charset=utf-8',
                success: handleResponse,
                headers: {
                    "X-CSRFToken": window.CSRF_TOKEN
                }
            });
        }
    });
});
