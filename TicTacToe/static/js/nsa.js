/*
# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.
*/

$(document).ready(function(){
    game_over = false;
    $(".cell").hover(function (){
        if (!game_over) {
            // Set the red X on every hover
            $(this).children().attr('src', '/static/img/red_x.png');
            // Parse the cell number from the selected cell ID
            var chosen = $(this).attr('id').substr(1,1);
            // Create the URL for the selected move
            var url = window.location + 'move/' + chosen + '/';
            // Collect all occupied cells for submission to the game API
            var occupied = getOccupied();
            $.getJSON(url, occupied, function(data) {
                if (data.over == true) {
                    game_over = true;
                }
                // If there is a winner, the game will be over so we turn on gray boxes for each winning cell
                $.each(data.result.result, function(key, val) {
                    $("#c" + val + "> .winner").css('visibility', 'visible');
                    $("#hdr_msg").html('I WIN!');
                });
            });
        } else {
            // Show a bit of cheek
            setTimeout(function() {
                $("#ftr_msg").html("" +
                    "(We're listening to your events; We <span style='font-style:italic'>always</span> know where you are...)");
            }, 1000)
        }
    });
});