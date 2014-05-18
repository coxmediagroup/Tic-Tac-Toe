"use strict"

var init_svg = function() {
    var g = d3.select("svg")
        .append('g')
        .attr("style", "stroke:black;stroke-width:10")
        .attr("id", "ttt_g")
    g.append('line').attr({x1: 200, y1:   0, x2: 200, y2: 600})
    g.append('line').attr({x1: 400, y1:   0, x2: 400, y2: 600})
    g.append('line').attr({x1:   0, y1: 200, x2: 600, y2: 200})
    g.append('line').attr({x1:   0, y1: 400, x2: 600, y2: 400})
    $.each(ttt_data.board, function( i, val ) {
        add_mark(i, val, true);
    });
}

var add_mark = function(position, mark, fast) {
    var g = d3.select("#ttt_g"),
        id = 'ttt_pos_' + position,
        x = position % 3,
        y = Math.floor(position / 3),
        top_x = 20 + 200 * x,
        top_y = 20 + 200 * y,
        width = 160,
        height = 160,
        bot_x = top_x + width,
        bot_y = top_y + width,
        r = (width / 2),
        ctr_x = top_x + r,
        ctr_y = top_y + r;
    $('#' + id).remove();
    var g_sub = g.append('g').attr('id', id);

    switch (mark) {
        case 0:
            /* User clicks to add their mark */
            g_sub
                .attr({class: 'tt_choice', style: "stroke:white"})
                .append('rect')
                .attr({
                    class: 'btn',
                    x: top_x,
                    y: top_y,
                    width: width,
                    height: height,
                    fill: "white",
                    onclick: "mark(\'" + position + "\')"
                })
            break;
        case 1:
            g_sub.attr('class', 'tt_x')
            g_sub.append('line')
                .attr({x1: top_x, y1: top_y, x2: bot_x, y2: bot_y})
            g_sub.append('line')
                .attr({x1: top_x, y1: bot_y, x2: bot_x, y2: top_y})
            break;
        case 2:
            g_sub.attr('class', 'tt_o')
            g_sub.append('circle')
                .attr({cx: ctr_x, cy: ctr_y, r: r, fill: 'white'})
            break;
    }
}

var update_winner = function() {
    var title = $('#body-title');
    if (title) {
        if (ttt_data.winner === 0) {
            title.text('Your turn.');
        } else if (ttt_data.winner === 3) {
            title.text("It's a tie!");
        } else if (ttt_data.winner === ttt_data.server_player) {
            title.text('Server wins!');
        } else {
            title.text('Player wins!');
        }

        if (ttt_data.winner !== 0){
            $('.tt_choice').remove()
            add_next();
        }
    }
}

var add_next = function() {
    $('.tt_next').removeClass("hidden");
}

var mark = function(position) {
    /* Report the user's choice and get the server's move */
    var user_mark = 1;
    if (ttt_data.server_player === 1) {
        user_mark = 2;
    }
    add_mark(position, user_mark);
    $.ajax(ttt_data.move_url, {data: {position: position}, type: 'POST'})
        .done(function(data) {
            $.each(data.board,  function( i, val ) {
                if (val !== ttt_data.board[i]) {
                    add_mark(i, val);
                }
            });
            ttt_data = data;
            update_winner();
        });
}

/* On initial load, create the board */
init_svg($('.tt_board'));
update_winner();
