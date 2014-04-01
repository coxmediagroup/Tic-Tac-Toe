/*
# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.
*/

$(document).ready(function(){
    var turn = 'human';
    var game_over = false;
    $(".cell").click(function() {
        /* *
         * Clicks always mean it's the human's turn (or was), but we toggle the "turn" variable to basically ignore
         * any clicks while the computer is processing so the human can't click until their turn
         * */
        if (turn == 'human') {
            turn = 'machine';
            // Turn on the blue O (human's piece)
            $(this).children().attr('src', '/static/img/blue_o.png');
            // Parse the chosen cell number from the ID
            var chosen = $(this).attr('id').substr(1,1);
            // Build the URL
            var url = window.location + 'move/' + chosen + '/';
            // Collect all occupied cells for submission to the game API
            var occupied = getOccupied();
            $.getJSON(url, occupied, function(data) {
                if (data.over == true) {
                    game_over = true;
                } else {
                    // Once we get to this point, it's safe to give the turn back to the human
                    turn = 'human';
                }
                if (data.result.result != 'draw') {
                    // Set the red X for the computers move
                    $("div[id=c" + data.move + "] > img").attr('src', '/static/img/red_x.png');
                    // If there is a win, turn on the grays for the winning cells
                    $.each(data.result.result, function(key, val) {
                        $("#c" + val + "> .winner").css('visibility', 'visible');
                        $("#hdr_msg").html('I WIN!');
                    });
                } else {
                    $("#hdr_msg").html("It's a draw!");
                }
            });
        } else {
            // Some attitude to show if the human click's when the game is over or it's the computers turn.
            if (game_over) {
                $("#hdr_msg").html('Uh...do you not know how to play this game?');
            } else {
                $("#hdr_msg").html('Hey, wait your turn!');
            }
        }
    });
});