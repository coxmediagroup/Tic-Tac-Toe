jQuery(function($)
{
    // create representations of board
    
    // first representation will be for display: includes both players, 0 for unplayed, 1 for X, 4 for O
    //top left element is board[0][0]
    var board = [[0,0,0],[0,0,0],[0,0,0]];
    
    // second representation is one array for each player, 0 for unplayed, 1 for X or O
    var Xboard = [[0,0,0],[0,0,0],[0,0,0]];
    var Oboard = [[0,0,0],[0,0,0],[0,0,0]];
    
    // third representation is single array, left to right in each row.   0 for unplayed, 1 for X, 4 for O
    var board_list = [0,0,0,0,0,0,0,0,0];
    var corners = [0,2,6,8];
    var opposite_corners = [8,6,2,0];
    
    var edges = [1,3,5,7];
    var center = 4;
    
    // This is all the three in a row wins:
    var three_in_rows = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    
    var users_turn = true;
    
    // cell user played most recently
    var last_user_cell_num = 14;
    
    var first_move = true;
    
    var num_for_X = 1;
    var num_for_O = 4;
    
    var computer_mark = '';
    var val_for_computer_mark = 0;
    var val_for_user_mark = 0;
    if (computer_first) {
        computer_mark = 'X';
        val_for_computer_mark = num_for_X;
        val_for_user_mark = num_for_O;
    } else {
        computer_mark = 'O';
        val_for_computer_mark = num_for_O;
        val_for_user_mark = num_for_X;
    }
    
    // this will be used by all the functions that look for situations, and return the cell to play or none.
    result = {found:false,cell_num:0};
    
    function mark_square(cell_num) {
        // marks the square cell_num with X or O as appropriate
        
        // if computers turn and computer first, X
        // if computers turn and user first, O
        // if users turn and computer first, O
        // if users turn and user first, X
        // There is probably a more elegant way to do this, TODO
        cell = $('#' + cell_num);
        if (users_turn) {
            if (computer_first) {
                cell.html('O');
                board_list[cell_num] = 4;
            } else {
                cell.html('X');
                board_list[cell_num] = 1;
            }
            last_user_cell_num = cell_num;
        } else {
            if (computer_first) {
                cell.html('X');
                board_list[cell_num] = 1;
            } else {
                cell.html('O');
                board_list[cell_num] = 4;
            }
        }
    }
    
    function win(val_for_mark) {
        // if there are two in a row and the third is empty, then find the third.
        // Adding row equals 2 (if I'm X) or 8 (if I'm O)
        result.found = false;
        for (var i = 0; i < three_in_rows.length; i++) {
            num_marks_in_row = 0;
            third_in_row = 0;
            row = three_in_rows[i];
            // see if I have two out of three of three_in_rows[i]
            for (var j = 0; j < row.length; j++) {
                if (board_list[row[j]] === val_for_mark) {
                    num_marks_in_row += 1;
                } else {
                    third_in_row = row[j];
                }
            }
            if (num_marks_in_row == 2 && board_list[third_in_row] === 0) {
                result.cell_num = third_in_row;
                result.found = true;
                return  // there may be more than one win, but return first one found
            }
        }
    }
    
    // logic for computer to make move
    function make_move() {
        users_turn = false;
        
        // if we're going first:
        if (computer_first && first_move) {
            // to simplify this, we're always going to select top left.
            // Could easily select random square, or random corner, etc.
            mark_square(0);
            first_move = false;
            users_turn = true;
            return;
        }
        
        // if user went first and it's my first move, then respond using book opening.   This may avoid needing the fork logic since it allows us to use force logic.
        if (!computer_first && first_move) {
            if (last_user_cell_num == 4) {
                // If user plays center, play corner.
                mark_square(0);
            } else {
                // If user plays corner or edge, play center.
                mark_square(4);
            }
            first_move = false;
            users_turn = true;
            return;
        }
        
        // ok, now for non-first moves:
        
        //1. Win: If the player has two in a row, play the third to get three in a row.
        win(val_for_computer_mark);
        if (result.found) {
            mark_square(result.cell_num);
            alert('I won!');
            users_turn = true;
            return;
        }
        //2. Block: If the [opponent] has two in a row, play the third to block them.
        win(val_for_user_mark);
        if (result.found) {
            mark_square(result.cell_num);
            users_turn = true;
            return;
        }
        //3. Fork: Create an opportunity where you can win in two ways.
        //4. Block opponent's Fork:
        //Option 1: Create two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork or winning. For example, if "X" has a corner, "O" has the center, and "X" has the opposite corner as well, "O" must not play a corner in order to win. (Playing a corner in this scenario creates a fork for "X" to win.)
        //Option 2: If there is a configuration where the opponent can fork, block that fork.
        //5. Center: Play the center.
        if (board_list[4] === 0) {
            mark_square(4);
            users_turn = true;
            return;
        }
        //6. Opposite corner: If the opponent is in the corner, play the opposite corner.
        for (var i = 0; i < corners.length; i++) {
            if (last_user_cell_num === corners[i]) {
                // user played a corner: play opposite corner
                mark_square(opposite_corners[i]);
                users_turn = true;
                return;
            } 
        }
        //7. Empty corner: Play in a corner square.
        for (var i = 0; i < corners.length; i++) {
            if (board_list[corners[i]] === 0) {
                mark_square(corners[i]);
                users_turn = true;
                return;
            } 
        }
        //8. Empty side: Play in a middle square on any of the 4 sides.
        for (var i = 0; i < edges.length; i++) {
            if (board_list[edges[i]] === 0) {
                mark_square(edges[i]);
                users_turn = true;
                return;
            } 
        }
    }
    
    if (computer_first) {
        make_move();        
    }
    
    function game_over() {
        for (var i = 0; i < board_list.length; i++) {
            if (board_list[i] === 0) {
                return false;
            }
        }
        return true;
    }
    
    // user input
    function select_square(cell) {
        // check if cell is already taken
        cell_num = cell.attr('id');
        if (board_list[cell_num] === 0) {
            mark_square(cell_num);
              // prevents user clicking two cells
            if (game_over()) {
                alert('Game over');
            }
            make_move();
            if (game_over()) {
                alert('Game over');
            }
        } else {
            alert('Sorry, that square is taken');
        }
    }

    // user input click handler
    $(".cell").click(function() {
        if (users_turn) {
            select_square($(this))
        }
    });
});
            
