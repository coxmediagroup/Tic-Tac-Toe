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
                        if (board[i] == 1) {
                            $('#' + i).html('X');
                        }
                        else if (board[i] == 2) {
                            $('#' + i).html('O');
                        }
                    });

                    // Write out the current game status to the DOM
                    status_game = data['status']
                    if (status_game == 1) {
                        status_game = "You've beaten the AI"; // This should never be executed
                    }
                    else if (status_game == 2) {
                        status_game = "the AI has beaten you";
                    }
                    else if (status_game == 3) {
                        status_game = "Tie game - click restart to play again";
                    }
                    else {
                        status_game = "No Result - keep playing!";
                    }
                    $('#game_status').text(status_game);

                    // If the game is over then disable the game board
                    if (status_game == 1 || status_game == 2 || status_game == 3) {
                        $("a[name='move']").preventDefault();
                    }
                }
            });
        });

    });

}(jQuery));
