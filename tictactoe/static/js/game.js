jQuery(function($)
{

    // user input
    function select_square(cell) {
        // check if cell is already taken
        
        // if not then place marker in it
        if (computer_first) {
            // user is O
            cell.html('O');
        } else {
            // user is X
            cell.html('X');
        }
    }

    var users_turn = true;
    
    $(".cell").click(function() {
        if (users_turn) {
            select_square($(this))
        }
    });

    // functions to create representations of board
    
});
            
