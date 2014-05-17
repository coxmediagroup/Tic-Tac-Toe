"use strict"

var make_svg = function(board) {
    /* Make the tic-tac-toe SVG */
    var svg = '<svg id="ttt_svg" height="600" width="600">',
        line_style = ' style="stroke:black;stroke-width:10" ';

    svg += '<line x1="200" y1="0" x2="200" y2="600"' + line_style + '/>';
    svg += '<line x1="400" y1="0" x2="400" y2="600"' + line_style + '/>';
    svg += '<line x1="0" y1="200" x2="600" y2="200"' + line_style + '/>';
    svg += '<line x1="0" y1="400" x2="600" y2="400"' + line_style + '/>';

    $.each(ttt_data.board, function( i, val ) {
        var top_x = 20 + 200 * (i % 3),
            top_y = 20 + 200 * (Math.floor(i / 3)),
            width = 160,
            bot_x = top_x + width,
            bot_y = top_y + width,
            r = (width / 2),
            ctr_x = top_x + r,
            ctr_y = top_y + r;

        switch (val) {
            case 0:
                /* User clicks to add their mark */
                svg += '<rect class="btn" x="' + top_x + '" y="' + top_y +
                       '" width="' + width + '" height="' + width +
                       '" fill="white" onclick="mark(\'' + i + '\')" />';
                break;
            case 1:
                svg += '<line x1="' + top_x + '" y1="' + top_y + '" x2="' +
                       bot_x + '" y2="' + bot_y + '" ' + line_style + '/>';
                svg += '<line x1="' + top_x + '" y1="' + bot_y + '" x2="' +
                       bot_x + '" y2="' + top_y + '" ' + line_style + '/>';
                break;
            case 2:
                svg += '<circle cx="' + ctr_x + '" cy="' + ctr_y + '" r="' +
                        r + '"' + line_style + ' fill="white" />';
                break;
        }
    });
    board.prepend(svg);
}

var update_winner = function() {
    var title = $('#body-title');
    if (title) {
        if (ttt_data.winner === 0) {
            if (ttt_data.next_moves.length === 0) {
                title.text("It's a tie!");
                add_next();
            } else {
                title.text('Your turn.');
            }
        } else if (ttt_data.winner === ttt_data.server_player) {
            title.text('Server wins!');
            add_next();
        } else {
            title.text('Player wins!');
            add_next();
        }
    }
}

var add_next = function() {
    $('.tt_next').removeClass("hidden");
}

var mark = function(position) {
    /* Report the user's choice and get the server's move */
    $.ajax(ttt_data.move_url, {data: {position: position}, type: 'POST'})
        .done(function(data) {
            var board = $('.tt_board');
            ttt_data = data;
            $('#ttt_svg').remove();
            make_svg(board);
            update_winner();
        });
}

/* On initial load, create the board */
make_svg($('.tt_board'));
update_winner();
