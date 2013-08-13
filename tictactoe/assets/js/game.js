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
        $('td').html('');
    });
});

function load_game(game_data) {
    $.each(game_data, function(index, value){
        $('#c' + index).html(value);
    });
}

// On load, reset game
$.get(reset_url);
