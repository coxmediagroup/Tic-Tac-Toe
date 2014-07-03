(function( $ ) {
    /**
     * Handle button clicks within the tic tac toe game board.
     */
    'use strict';

    $.fn.TicTacToe = function () {
        $.each($.find("input[type=submit]"), function() {
            $(this).on('click', function(e) {
                e.preventDefault();
                console.log($(this).attr('name'));
            });
        });


        return this;
    }
}(jQuery));