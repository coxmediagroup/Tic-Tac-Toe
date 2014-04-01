/*
# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.
*/

$(document).ready(function(){
    var game_over = false;
    $(".cell").click(function() {
        if (game_over) {
            return false;
        }
        $(this).children().attr('src', '/static/img/blue_o.png');
        var chosen = $(this).attr('id').substr(1,1);
        var url = window.location + 'move/' + chosen + '/';
        $.getJSON(url, function(data) {
            $.each(data.winner, function(key, val) {
                $("div[id=c" + val + "] > img").attr('src', '/static/img/red_x.png');
                $("#c" + val + "> .winner").css('visibility', 'visible');
                $("#hdr_msg").html('I WIN!');
            });
        });
        game_over = true;
        setTimeout( function() {
            $("#ftr_msg").html('Hey, the instructions just said "never lose," they never said I had to follow the rules...')}
            , 3000
        );
    });
});