(function($) { // creating local namespace and use 'no conflict' mode

    $(document).ready(function() {

        var board = [0,0,0,0,0,0,0,0,0];

        $('a[name=move]').bind('click', function() { 
            index = $(this).attr('id');
            board[index] = 1
            $.ajax({
                url: "/ajax/make_a_move/",
                type: "GET",
                data: {'board': JSON.stringify(board)},
                success: function(data) {
                    // for each item in data['board'] fill in the corresponding game board table cell
                    board = data
                    $.each(board, function(i) {
                        if (board[i] == 1) {
                            $('#' + i).html('X');
                        }
                    });
                }
            });
        });

    });

}(jQuery));
