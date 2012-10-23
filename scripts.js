// Initiate game
$(document).ready(init_cells);

// Bind click event
function init_cells() {
    $('.board td').click(take_turn);
}

// Variable to hold the current player
var current_player = 'X';

// Information about each plyaer
var players = {
    'X': { 
        'opponent': 'O',
        'value': 1
    },
    'O': { 
        'opponent': 'X',
        'value': -1
    },
}

// A reference to each possible winning lineup of game cells
var lines = {
    0: $('#3,#5,#7'), // Horizontal up
    1: $('#1,#2,#3'), // Row 1
    2: $('#4,#5,#6'), // Row 2
    3: $('#7,#8,#9'), // Row 3
    4: $('#1,#5,#9'), // Horizontal down
    5: $('#1,#4,#7'), // Column 1
    6: $('#2,#5,#8'), // Column 2
    7: $('#3,#6,#9')  // Column 3
}

// Handle a turn, check for a winner, and if it's the computer's 
// turn next then have the computer take a turn
function take_turn(event) {
    // Get the clicked cell
    var $cell = $(this);
    if ($cell.html().trim() == '') {
        // If they clicked on an empty cell then set the contents
        // of the cell to their player symbol and set the value 
        // of the cell to their value (X=1, O=-1).
        $cell.html(current_player);
        $cell.attr('value', players[current_player].value);

        // Swap the current_player variable
        current_player = players[current_player].opponent;

        // Check for a winner
        check_for_winner();

        // If it's the computer's turn, make a move
        if (current_player == 'O') {
            auto_play();
        }
    }
}

// Handle taking a turn as the computer
function auto_play() {
    var rows = get_game_state();
    for (index in rows) {
        var row = rows[index];
        if (Math.abs(row) > 1) {
           var blocking_cell = lines[index].filter('[value="0"]'); 
           $(blocking_cell).click();
           return;
        }
    }
    // Get a random corner
    $('#1, #3, #7, #9')
        .filter('[value="0"]')
        .get()
        .sort(function() { 
                return Math.round(Math.random())-.5;
            })[0]
        .click();
}

// See if anyone has won yet, and if so mark the winning line in red
function check_for_winner() {
    var rows = get_game_state();
    for (index in rows) {
        var row = rows[index];
        if (Math.abs(row) > 2) {
           lines[index].css({'color': 'red'}); 
           current_player = '';
           break;
        }
    }
    if ($('.board td[value="0"]').length == 0) {
        // Game over
        current_player = '';
    }
}

// Get a list of line states so we can calculate if someone has won
// and what the next computer move should be
function get_game_state() {
    var rows = [];
    for (index in lines) {
        // Get the score of the current line
        rows.push(get_score(lines[index]));
    }
    return rows;
}

// Calculate the score of the passed in line of cells. A score is
// the sum of the values of each cell (X=1, O=-1, empty=0) 
function get_score(cells) {
    var output = 0;
    $(cells).each(function(i, o) {
        var value = parseInt($(o).attr('value'));
        output += value;
    });
    return output;
}
