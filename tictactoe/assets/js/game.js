$('td').click(function(){
    var val = $(this).html();
    if (val) {
        alert('This square contains an ' + val + '. Please try another square.');
    }
    else {
        var clicked = $(this).data('number');
        $.get(next_move_url, {clicked: clicked}, function(data){
            load_game(data);
        });
    }
});

$('.try-again').click(function(){
    $.get(reset_url, {}, function(data){
        $('td').html('').removeClass('highlight');
    });
});

function load_game(game_data) {
    $.each(game_data['game'], function(index, value){
        $('#c' + index).html(value);
    });
    if (game_data['winning_combo']) {
        $.each(game_data['winning_combo'], function(index, value){
            $('#c' + value).addClass('highlight');
        });
    }
}

// On load, reset game
$.get(reset_url);
