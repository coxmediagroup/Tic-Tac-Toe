
$(document).ready(init_cells);

var current_player = 'X';

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

function init_cells() {
    
    $('.board td').click(take_turn);
}

function take_turn(event) {
    var $cell = $(this);
    if ($cell.html().trim() == '') {
        $cell.html(current_player);
        $cell.attr('value', players[current_player].value);
        current_player = players[current_player].opponent;
    }
    check_for_winner();
}

function check_for_winner() {
    var rows = get_game_state();
    for (index in rows) {
        var row = rows[index];
        if (Math.abs(row) > 2) {
           lines[index].css({'background-color': 'blue'}); 
        }
    }
}

function total(total, value) {
    return total+value;
}

function get_game_state() {
    var rows = [];
    for (index in lines) {
        rows.push(get_score(lines[index]));
    }
    return rows;
}

function get_score(cells) {
    var output = 0;
    $(cells).each(function(i, o) {
        var value = parseInt($(o).attr('value'));
        if (!isNaN(value)) {
            output += value;
        }
    });
    return output;
}
