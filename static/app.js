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
                        $.each(data.win_lines, function (idx, line) {
                            $.each(line, function (idx, cell) {
                                $($($('.grid .row')[cell.y]).find('.cell')[cell.x]).addClass('win');
                            });
                        });
                        $('.grid').removeClass('enabled');
                    }
                }
            })
        },

        gridReset = function () {
            $('.grid').addClass('enabled');
            $('.grid .cell').removeClass('filled win').text('');
        },
        
        addMark = function (x, y, mark) {
            $($($('.grid .row')[y]).find('.cell')[x]).addClass('filled').text(mark);
        };

    $('#newGame').click(function () {
        $.ajax({
            url: '/start', 
            success: function () {
                gridReset();
            },
        });
    });

    $('.content').on('click', '.grid.enabled .cell:not(.filled)', function () {
        var x = $(this).index(),
            y = $(this).parent('.row').index();
        userMove(x, y);
    });
});