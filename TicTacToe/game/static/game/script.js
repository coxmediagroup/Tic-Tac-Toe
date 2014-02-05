/**
 * Created by Lehel on 2/5/14.
 */
var canClick = true;
var xImagePath = "";
var oImagePath = "";
var context;
var ajaxUrl = "";

function updateBoard(data) {

    var game_state = '';
    var winner = '';
    var message = '';

    for (var key in data) {

        var val = data[key];

        if(key.substr(0, 3) == "box") {
            $("#" + key).empty();
            if(val == 'X')
                $("#" + key).prepend('<img src="' + xImagePath + '" />');
            else if(val == 'O')
                $("#" + key).prepend('<img src="' + oImagePath + '" />');
        }

        if(key == 'game_state')
            game_state = val;
        if(key == 'winner')
            winner = val;
        if(key == 'message')
            message = val;
    }

    if(game_state == 'OVER') {
        if(winner == 0)
            winner = 'You have won!';
        else if(winner == 1)
            winner = 'The Computer has beat you!';
        else
            winner = 'The game is a draw!';

        $("#message").html(winner);
    }
    else
        $("#message").html(message);
}

$(document).ready(function() {

    updateBoard(context);

    $("#board div").click(function() {
        var box = this;

        if(canClick) {
            canClick = false;
            var newUrl = ajaxUrl.replace("/12345/", "/" + $(box).attr('id').substring(3,4));
            $.getJSON(newUrl, function( data ) {
                updateBoard(data);
                canClick = true;
            });
        }
    });



});
