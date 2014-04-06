var TicTacToeCtrl = (function($, undefined) {
    var self = {},
        game_name = null,
        game_number = 1,
        game_id = null,
        name_button = $("#name-button");

    // Register event handlers once the page is ready.
    function init() {
        $(document).ready(function() {
            $('#name').on('keyup blur',function(evt) {
                if(evt.target.value.length > 0) {
                    name_button.prop('disabled', false);
                    game_name = evt.target.value;
                } else {
                    name_button.prop('disabled', true);
                    game_name = null;
                }
            });

            $('.board td').click(function(evt) {
                var square = $(evt.target);
                var x = square.data('x');
                var y = square.data('y');

                if(square.text() === "") {
                    square.html('X');
                    make_move(x, y);
                }
            });

            name_button.click(start_game);
        });
    }

    function make_move(x,y) {
        console.log("Make move " + x + "," + y);
    }

    // Start the game by fetching the new game id from the server.
    function start_game() {
        name_button.prop('disabled', true);
        $.post('/api/new-game/', { name: game_name}, function(data) {
            game_id = data.id;
            $('.jumbotron').fadeOut("fast", function() {
                $(".player-name > span").text(game_name);
                $(".player-name").removeClass('hidden');
                $(".board").removeClass('hidden');
            });
        });
    }

    init();

    return self;
})($);