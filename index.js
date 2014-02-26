/*
 * A complete tic-tac-toe widget.  Just include this script in a
 * browser page and enjoy.  A tic-tac-toe game will be included
 * as a child element of the element with id "tictactoe".  If the
 * page has no such element, it will just be added at the end of
 * the body.
 */
(function () {

    var squares = [], 
        EMPTY = "\xA0",
        score,
        moves,
        turn = "X",
        oldOnload,

    /*
     * To determine a win condition, each square is "tagged" from left
     * to right, top to bottom, with successive powers of 2.  Each cell
     * thus represents an individual bit in a 9-bit string, and a
     * player's squares at any given time can be represented as a
     * unique 9-bit value. A winner can thus be easily determined by
     * checking whether the player's current 9 bits have covered any
     * of the eight "three-in-a-row" combinations.
     *
     *     273                 84
     *        \               /
     *          1 |   2 |   4  = 7
     *       -----+-----+-----
     *          8 |  16 |  32  = 56
     *       -----+-----+-----
     *         64 | 128 | 256  = 448
     *       =================
     *         73   146   292
     *
     */
    wins = [7, 56, 448, 73, 146, 292, 273, 84],

    blockIndices = {
        7:   [0, 1, 2],
        56:  [3, 4, 5],
        448: [6, 7, 8],
        73:  [0, 3, 6],
        146: [1, 4, 7],
        292: [2, 5, 8],
        273: [0, 4, 8],
        84:  [2, 4, 6]
    },

    /*
     * Clears the score and move count, erases the board, and makes it
     * X's turn.
     */
    startNewGame = function () {
        var i;
        
        turn = "X";
        score = {"X": 0, "O": 0};
        moves = 0;
        for (i = 0; i < squares.length; i += 1) {
            squares[i].firstChild.nodeValue = EMPTY;
        }
    },

    /*
     * Returns whether the given score is a winning score.
     */
    win = function (score) {
        var i;
        for (i = 0; i < wins.length; i += 1) {
            if ((wins[i] & score) === wins[i]) {
                return true;
            }
        }
        return false;
    },

    computer = function(e) {
        var maximumMatch = 0;
        var idx;
        for (i = 0; i < wins.length; i += 1) {
            var match = wins[i] & score['X'];
            var blocked = match | (wins[i] & score['O']);
            
            // If a win is already not blocked, and current win possiblity is greater, store it
            if((blocked !== wins[i]) && (countOneWeightsInIntOnRadix2(match) > countOneWeightsInIntOnRadix2(maximumMatch))) {
                maximumMatch = match;
                idx = i;
            }            
        }

        // After finding our target win to block, we need to determine which exact index we are going to block
        // This elaborate algorithm exactly does that.

        var blockIdx = blockIndices[wins[idx]];
        console.log("REQ block at: " + blockIdx);

        var blockKeys = [];
        for (var i = 0; i < blockIdx.length; i++) {
            blockKeys.push({
                row: parseInt(blockIdx[i]/3),
                col: blockIdx[i] % 3
            })
        }

        console.log("Opponent moved: " + e.row + ', ' + e.col);
        var opPrevMove = {row: e.row, col: e.col};
        var targetMove;
        var targetMoveSelector;

        // Determine the block key with the lowest possible loseQuotient
        for (var i in blockKeys) {
            var move = {
                row: blockKeys[i].row,
                col: blockKeys[i].col
            };
            var moveQuery = {row: 'row=', col: 'col='};
            moveQuery.row += move.row;
            moveQuery.col += move.col;
            var selector = '[' + moveQuery.row + ']' + '[' + moveQuery.col + ']';
            if ($(selector).text() === EMPTY) {
                if (!targetMove || (loseQuotient(targetMove, opPrevMove) > loseQuotient(move, opPrevMove))) {
                    targetMove = move;
                    targetMoveSelector = selector;
                }
            }
        }
        
        console.log('(' + targetMove.row + ', ' + targetMove.col + ')');
        $(targetMoveSelector).trigger('click');
    },

    /*
     * Sets the clicked-on square to the current player's mark,
     * then checks for a win or cats game.  Also changes the
     * current player.
     */
    set = function () {
        if (this.firstChild.nodeValue !== EMPTY) {
            return;
        }
        this.firstChild.nodeValue = turn;
        moves += 1;
        score[turn] += this.indicator;
        if (win(score[turn])) {
            alert(turn + " wins!");
            startNewGame();
        } else if (moves === 9) {
            alert("Cat\u2019s game!");
            startNewGame();
        } else {
            turn = turn === "X" ? "O" : "X";
        }

        if (turn === "O") {
            var event = jQuery.Event( "human" );
            event.row = this.getAttribute('row');
            event.col = this.getAttribute('col');
            $( "body" ).trigger( event );
        }
    },

    /*
     * Creates and attaches the DOM elements for the board as an
     * HTML table, assigns the indicators for each cell, and starts
     * a new game.
     */
    play = function () {
        var board = document.createElement("table"),
            indicator = 1,
            i, j,
            row, cell,
            parent;
        board.border = 1;
        for (i = 0; i < 3; i += 1) {
            row = document.createElement("tr");
            board.appendChild(row);
            for (j = 0; j < 3; j += 1) {
                cell = document.createElement("td");
                cell.setAttribute('row', i);
                cell.setAttribute('col', j);
                cell.width = cell.height = 50;
                cell.align = cell.valign = 'center';
                cell.indicator = indicator;
                cell.onclick = set;
                cell.appendChild(document.createTextNode(""));
                row.appendChild(cell);
                squares.push(cell);
                indicator += indicator;
            }
        }

        // Attach under tictactoe if present, otherwise to body.
        parent = document.getElementById("tictactoe") || document.body;
        parent.appendChild(board);
        startNewGame();
    };

    /*
     * Add the play function to the (virtual) list of onload events.
     */
    if (typeof window.onload === "function") {
        oldOnLoad = window.onload;
        window.onload = function () {
            oldOnLoad(); 
            play();
        };
    } else {
        window.onload = play;
    }

    // Register human event that will trigger the computer move
    $(document.body).on('human', computer);
}());

// Calculates a quotient using a prospective move and previous opponent move
// Basically, a measure of closeness - close moves lead to no possiblities for opponent wining
function loseQuotient(move, opPrevMove) {
    console.dir(move);
    console.log(Math.abs(move.row - opPrevMove.row) + Math.abs(move.col - opPrevMove.col));
    return Math.abs(move.row - opPrevMove.row) + Math.abs(move.col - opPrevMove.col);
}

// Since the score of each component in a 9-bit integer, counting number of 1s in its radix-2 form is useful
// for measuring the state of the tic-tac-toe board
function countOneWeightsInIntOnRadix2(number) {
    var total = 0;
    while (number != 0) {
        total += (number % 2);
        number = parseInt(number / 2);
    }
    return total;
}
