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
            $(this).children().attr('src', '/static/img/red_x.png');
            var chosen = $(this).attr('id').substr(1,1);
            var url = window.location + 'move/' + chosen + '/';
            var occupied = getOccupied();
            $.getJSON(url, occupied, function(data) {
                if (data.over == true) {
                    game_over = true;
                }
                $.each(data.result.result, function(key, val) {
                    $("#c" + val + "> .winner").css('visibility', 'visible');
                    $("#hdr_msg").html('I WIN!');
                });
            });
        } else {
            setTimeout(function() {
                $("#ftr_msg").html("" +
                    "(We're listening to your events; We <span style='font-style:italic'>always</span> know where you are...)");
            }, 1000)
        }
    });
});