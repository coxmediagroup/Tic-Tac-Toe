function make_move(cell_idx) {
    $.post(
        '/move',
        {cell: cell_idx},
        function(data, textStatus, jqXHR) {
            if(data.status && data.move !== null) {
                $('#board .cell').eq(data.move).addClass('o');
            } else {
                if(data.status == false && data.msg == "Invalid game.") {
                    $('#new-game').click();
                }
            }
            
            if(data.state == "win") {
                increment_losses();
                alert("You lose!")
            }
            
            if(data.state == "draw") {
                increment_draws();
                alert("Draw!");
            }
            
            console.log(data);
        },
        'json'
    );
}

$(function() {
    // code goes here
    $('#board .cell').each(
        function(idx, e) {
            $(e).click(idx, function(evt) {
                // idx.data now holds the cell number
                if($(this).hasClass('x') || $(this).hasClass('o')) {
                    return;     // do nothing
                }
                $('#board .cell').eq(evt.data).addClass('x');
                make_move(evt.data);
            });
        }
    );
    $.get('/get_details', function(data, textStatus, jqXHR) {
        var board = data.board;
        var draws = data.draw_count;
        var games = data.game_count;
        var losses = data.game_count - data.draw_count;
        $('#draws').html(draws);
        $('#losses').html(losses);
        for(var i = 0; i < 9; i++) {
            if(board[i] != " ") {
                $('#board .cell').eq(i).addClass(board[i]);
            }
        }
    }, 'json');
    $('#new-game').click(function(evt) {
        $.get('/new_game', function(data, textStatus, jqXHR) {
            if(!data.status) {
                alert("Error resetting game.  Please try again.");
                return;
            }
            $('#board .cell').removeClass("x");
            $('#board .cell').removeClass("o");
        }, 'json');
    });
});

function increment_losses() {
    $('#losses').html(parseInt($('#losses').html()) + 1);
}

function increment_draws() {
    $('#draws').html(parseInt($('#draws').html()) + 1);
}

