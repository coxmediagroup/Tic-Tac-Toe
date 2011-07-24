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
    
    // user input
    function select_square(cell) {
        // check if cell is already taken
        cell_num = cell.attr('id');
        if (board_list[cell_num] === 0) {
            // place marker in it
            if (computer_first) {
                // user is O
                cell.html('O');
                board_list[cell_num] = 4;
            } else {
                // user is X
                cell.html('X');
                board_list[cell_num] = 1;
            }
        } else {
            alert('Sorry, that square is taken');
        }
    }

    var users_turn = true;
    
    $(".cell").click(function() {
        if (users_turn) {
            select_square($(this))
        }
    });

    
    
});
            
