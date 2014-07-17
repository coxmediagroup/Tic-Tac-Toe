(function($) { // creating local namespace and use 'no conflict' mode

    $(document).ready(function() {

        board = [0,0,0,0,0,0,0,0,0];

        $('a[name=move]').bind('click', function() { 
            index = $(this).attr('id');
            board[index] = 1;
            $.ajax({
                url: "/ajax/make_a_move/",
                type: "GET",
                data: {'board': JSON.stringify(board)},
                success: function(data) {

                    // for each item in data['board'] fill in the corresponding game board table cell
                    board = data['board']
                    $.each(board, function(i) {
                        space = $('#space_' + i)
                        if (board[i] == 1) {
                            space.html('X');
                        }
                        else if (board[i] == 2) {
                            space.html('O');
                        }
                    });

                    // Write out the current game status to the DOM
                    game_status = data['status'];
                    game_status_text = ''; 
                    if (game_status == 1) {
                        game_status_text = "You've beaten the AI"; // This should never be executed
                    }
                    else if (game_status == 2) {
                        game_status_text = "the AI has beaten you";
                    }
                    else if (game_status == 3) {
                        game_status_text = "Tie game - click restart to play again";
                    }
                    else {
                        game_status_text = "No Result - keep playing!";
                    }
                    $('#game_status').text(game_status_text);

                    // If the game is over then disable the remaining space links
                    if (game_status == 1 || game_status == 2 || game_status == 3) {
                        $("a[name='move']").parent().html('');
                    }
                }
            });
        });

    });

}(jQuery));
