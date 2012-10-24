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
var corner_controls = $('#1, #3, #7, #9');

// Handle a turn, check for a winner, and if it's the computer's 
// turn next then have the computer take a turn
function take_turn(event) {
    // Get the clicked cell
    var $cell = $(this);
    if ($cell.html() == '' && current_player != '') {
        // If they clicked on an empty cell then set the contents
        // of the cell to their player symbol and set the value 
        // of the cell to their value (X=1, O=-1).
        $cell.html(current_player);
        $cell.attr('value', players[current_player].value);

        // Check for a winner
        if (!check_for_winner()) {

            // Swap the current_player variable
            current_player = players[current_player].opponent;

            // If it's the computer's turn, make a move
            if (current_player == 'O') {
                auto_play();
            }
        }
    }
}

// Handle taking a turn as the computer
function auto_play() {
    var rows = get_game_state();

    // Check each of the possible lines of cells and see if any of them
    // have two in a row. It's possible to have more than one such line
    var blocking_cells = [];
    for (index in rows) {
        var row = rows[index];
        if (Math.abs(row) > 1) {
           var blocking_cell = lines[index].filter('[value="0"]'); 
           blocking_cells.push({ 'cell': blocking_cell, 'row': row });
        }
    }
    if (blocking_cells.length == 1) {
        $(blocking_cells[0].cell).click();
        return;
    }
    // If there are two lines with two in a row, block or win 
    // but win above block, otherwise you could end up losing
    else if (blocking_cells.length > 1) {
        // Loop through the lines with two in a row and find the one
        // that would cause a win for the computer
        for (index in blocking_cells) {
            var row = blocking_cells[index].row;
            if (row < 0) { // O's are -1, X's are 1
                $(blocking_cells[index].cell).click();
                return
            }
        }
        // Do both winning possibilities belong to the player?
        // Seems unlikely, but just in case, block the first one
        $(blocking_cells[0].cell).click();
        return;
    }
    // If the player starts with a corner, take center
    if ($('#5').attr('value') == "0") {
        $('#5[value="0"]').click();
        return;
    }
    // If the player has two corners and the computer has center,
    // go for a win across or down, otherwise the player will win
    if (corner_controls.filter('[value="1"]').length == 2) {
        $('#2, #4, #6, #8').filter('[value="0"]:first').click();
        return;
    }

    // Get a random corner, unless the other player started in a corner,
    // in which case get the opposite corner, otherwise they will win
    var corners = {1:9, 3:7, 9:1, 7:3};
    var adjacent_cells_map = {
        "1": $("#2,#4"), 
        "3": $("#2,#6"),
        "7": $("#4,#8"),
        "9": $("#8,#6")
    };
    for (corner in corners) {
        var other_corner = corners[corner];
        if ($('#' + corner + '[value="1"], #' + other_corner + '[value="0"]').length == 2) {
            $('#' + other_corner).click();
            return;
        }
    }
    // Usually if all of the corners are taken up there are two in a 
    // row somewhere, but just to be sure, check for an available
    // corner, and if there are none then grab a random empty cell
    var available_corners = corner_controls
        .filter('[value="0"]')
        .get()
        .sort(function() { 
                return Math.round(Math.random())-.5;
            });
    // So, generally taking the center when possible and from there 
    // taking corners is a good strategy, if the player doesn't take 
    // center and the computer does, and then the computer's next move
    // is not adjacent to one of the player's moves, the player can win
    if (available_corners.length > 0) {
        for (index in available_corners) {
            var available_corner = available_corners[index];
            var adjacent_cells = adjacent_cells_map[$(available_corner).attr('id')];
            if (adjacent_cells.filter('[value="1"]').length > 0) {
                $(available_corner).click();
                return;
            }
        }
        $(available_corners[0]).click();
    }
    else {
        $('.board td[value="0"]:first').click();
    }
}

// See if anyone has won yet, and if so mark the winning line in red
function check_for_winner() {
    var rows = get_game_state();
    for (index in rows) {
        var row = rows[index];
        if (Math.abs(row) > 2) {
           lines[index].css({'color': 'red'}); 
           $('.winner').html(current_player + ' wins!');
           current_player = '';
           return true;
        }
    }
    if ($('.board td[value="0"]').length == 0) {
        // Game over
        $('.winner').html('Draw!');
        current_player = '';
        return true;
    }
    return false;
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
