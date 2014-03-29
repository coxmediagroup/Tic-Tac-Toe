$(document).ready(function(){
    var turn = 'human';
    var game_over = false;
    $(".cell").click(function() {
        if (turn == 'human') {
            turn = 'machine';
            $(this).children().attr('src', '/static/img/blue_o.png');
            var chosen = $(this).attr('id').substr(1,1);
            var url = window.location + 'move/' + chosen + '/';
            var occupied = getOccupied();
            $.getJSON(url, occupied, function(data) {
                if (data.over == true) {
                    game_over = true;
                } else {
                    turn = 'human';
                }
                if (data.result.result != 'draw') {
                    $("div[id=c" + data.move + "] > img").attr('src', '/static/img/red_x.png');
                    $.each(data.result.result, function(key, val) {
                        $("#c" + val + "> .winner").css('visibility', 'visible');
                        $("#msg").html('I WIN!');
                    });
                } else {
                    $("#msg").html("It's a draw!");
                }
            });
        } else {
            if (game_over) {
                $("#msg").html('Uh...do you not know how to play this game?');
            } else {
                $("#msg").html('Hey, wait your turn!');
            }
        }
    });
});

function getOccupied() {
    var occupied = {};
    var o = '';
    var x = '';
    $(".cell").each(function() {
        var cell = $(this).attr('id').substr(1,1);
        var src = $(this).children().attr('src');
        if (src != '/static/img/blank.png') {
            if (src == '/static/img/blue_o.png') {
                o += cell + ',';
            } else {
                x += cell + ',';
            }
        }
    });
    occupied['x'] = x;
    occupied['o'] = o;
    return occupied;
}