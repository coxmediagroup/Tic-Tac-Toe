$(function () {
    var userMark = 'x',
        aiMark = 'o',
        userMove = function (x, y) {
            $.ajax({
                url: '/move',
                data: {x: x, y: y},
                success: function (data) {
                    addMark(x, y, userMark);
                    if (data.ai_move) {
                        addMark(data.ai_move.x, data.ai_move.y, aiMark);
                    }
                    if (data.game_over) {
                        alert(data.message);
                        $('.grid').removeClass('grid_enabled');
                    }
                }
            })
        },
        gridReset = function () {
            $('.grid').addClass('grid_enabled');
            $('.grid .cell').text('');
        },
        addMark = function (x, y, mark) {
            $($($('.grid .row')[y]).find('.cell')[x]).text(mark);
        };

    $('#newGame').click(function () {
        $.ajax({
            url: '/start', 
            success: function () {
                gridReset();
            },
        });
    });

    $('.content').on('click', '.grid_enabled .cell:not(.filled)', function () {
        var x = $(this).index(),
            y = $(this).parent('.row').index();
        userMove(x, y);
    });
});