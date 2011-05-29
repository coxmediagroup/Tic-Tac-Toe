$('document').ready(function() {
    $('td').click(function () {
        var td = $(this);
        if (td.html().indexOf('X') == -1 && td.html().indexOf('O') == -1) {
            td.html("<h1>" + window.AVATAR + "</h1>");
        }
        var x = td.attr('x');
        var y = td.attr('y');
        $.post('/move/', {'x':x, 'y':y}, function(res) {
            var msg = $('#message')
            if (res['condition'] == 'error') {
                msg.css('text-color', 'red').html('Error: ' + res['message']);
                msg.show();
            }
            else {
                if (typeof(res['move']) != "undefined" && 
                    res['move'] != null) {
                    var move = res['move'];
                    var el = $('td[x=' + move[0] + '][y=' + move[1] + ']');
                    el.html('<h1>' + res['avatar'] + '</h1>');
                }
            }

            if (res['condition'] == 'Tie') {
                msg.css('text-color', 'black').html('Tie!');
                msg.show();
            }
            else if (res['condition'] == 'Win') {
                msg.css('text-color', 'black');
                msg.html('Player ' + res['avatar'] + ' won!');
                msg.show();
            }

        }, "json");
    });
})
