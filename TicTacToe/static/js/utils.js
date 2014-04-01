/*
# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.
*/

function getOccupied() {
    /** Return all the occupied positions on the board for both players **/
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