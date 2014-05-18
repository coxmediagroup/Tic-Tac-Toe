/*jslint browser: true */
/*global $, d3, ttt_data: true */
/*properties
    PI, ajax, append, arc, attr, attrTween, board, call, class, cx, cy, data,
    datum, delay, done, each, endAngle, fill, floor, height, innerRadius,
    interpolate, move_url, onclick, outerRadius, position, r, remove,
    removeClass, select, server_player, startAngle, style, svg, text, transition,
    type, width, winner, x, x1, x2, y, y1, y2
*/

var mark = (function () {
    'use strict';

    // Creates a tween on the specified transition's "d" attribute, transitioning
    // any selected arcs from their current angle to the specified new angle.
    // From http://bl.ocks.org/mbostock/5100636
    function arcTween(transition, arc, newAngle) {
        transition.attrTween("d", function (d) {
            var interpolate = d3.interpolate(d.endAngle, newAngle);
            return function (t) {
                d.endAngle = interpolate(t);
                return arc(d);
            };
        });
    }

    function add_mark(position, mark, fast) {
        var g = d3.select("#ttt_g"),
            id = 'ttt_pos_' + position,
            x = position % 3,
            y = Math.floor(position / 3),
            top_x = 20 + 200 * x,
            top_y = 20 + 200 * y,
            width = 160,
            bot_x = top_x + width,
            bot_y = top_y + width,
            g_sub,
            r,
            ctr_x,
            ctr_y,
            arc;
        $('#' + id).remove();
        g_sub = g.append('g').attr('id', id);

        switch (mark) {
        case 0:
            /* User clicks to add their mark */
            g_sub
                .attr({class: 'tt_choice', style: "stroke:none"})
                .append('rect')
                .attr({
                    class: 'btn',
                    x: top_x,
                    y: top_y,
                    width: width,
                    height: width,
                    fill: "white",
                    onclick: "mark(\'" + position + "\')"
                });
            break;
        case 1:
            g_sub.attr('class', 'tt_x');
            if (fast) {
                g_sub.append('line')
                    .attr({x1: top_x, y1: top_y, x2: bot_x, y2: bot_y});
                g_sub.append('line')
                    .attr({x1: top_x, y1: bot_y, x2: bot_x, y2: top_y});
            } else {
                g_sub.append('line')
                    .attr({x1: top_x, y1: top_y, x2: top_x, y2: top_y})
                    .transition(250)
                    .attr({x2: bot_x, y2: bot_y});
                g_sub.append('line')
                    .attr({x1: bot_x, y1: top_y, x2: bot_x, y2: top_y})
                    .transition(250).delay(300)
                    .attr({x2: top_x, y2: bot_y});
            }
            break;
        case 2:
            r = (width / 2);
            ctr_x = top_x + r;
            ctr_y = top_y + r;
            g_sub.attr('class', 'tt_o');
            if (fast) {
                g_sub.append('circle')
                    .attr({cx: ctr_x, cy: ctr_y, r: r, fill: 'none'});
            } else {
                arc = d3.svg.arc()
                    .innerRadius(r)
                    .outerRadius(r)
                    .startAngle(0);
                g_sub.attr('transform', 'translate(' + ctr_x + ',' + ctr_y + ')');
                g_sub.append('path')
                    .datum({endAngle: 0.1})
                    .attr("d", arc)
                    .transition(500)
                    .call(arcTween, arc, 2 * Math.PI);
            }
            break;
        }
    }

    function init_svg() {
        var g = d3.select("svg")
            .append('g')
            .attr("style", "stroke:black;stroke-width:10")
            .attr("fill", "none")
            .attr("id", "ttt_g");
        g.append('line').attr({x1: 200, y1:   0, x2: 200, y2: 600});
        g.append('line').attr({x1: 400, y1:   0, x2: 400, y2: 600});
        g.append('line').attr({x1:   0, y1: 200, x2: 600, y2: 200});
        g.append('line').attr({x1:   0, y1: 400, x2: 600, y2: 400});
        $.each(ttt_data.board, function (i, val) {
            add_mark(i, val, true);
        });
    }

    function add_next() {
        $('.tt_next').removeClass("hidden");
    }

    function update_winner() {
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

            if (ttt_data.winner !== 0) {
                $('.tt_choice').remove();
                add_next();
            }
        }
    }

    function mark(position) {
        /* Report the user's choice and get the server's move */
        var user_mark = 1;
        if (ttt_data.server_player === 1) {
            user_mark = 2;
        }
        add_mark(position, user_mark);
        ttt_data.board[position] = user_mark;

        setTimeout(function () {
            $.ajax(ttt_data.move_url, {data: {position: position}, type: 'POST'})
                .done(function (data) {
                    $.each(data.board, function (i, val) {
                        if (val !== ttt_data.board[i]) {
                            add_mark(i, val);
                        }
                    });
                    ttt_data = data;
                    update_winner();
                });
        }, 250);
    }

    /* On initial load, create the board */
    init_svg();
    update_winner();
    return mark;
}());
