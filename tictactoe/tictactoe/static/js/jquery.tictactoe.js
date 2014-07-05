(function( $ ) {
    /**
     * Handle button clicks within the tic tac toe game board.
     */
    'use strict';

    $.fn.TicTacToe = function () {
        $.each($.find("input[type=submit]"), function() {
            $(this).on('click', function(e) {
                e.preventDefault();
                setStatus();

                var $this = $(this),
                    $form = $(this.form),
                    data = $form.serialize();

                $.ajax({
                    url: $form.attr('action'),
                    type: $form.attr('method'),
                    data: data + "&move=" + $this.attr('name').split('-')[1],
                    success: function (data) {
                        if(!data.success) {
                            setStatus(data.message);
                        } else {
                            // check for a winner
                            switch (data.game.winner) {
                                case 'x':
                                    setStatus("Doh! Looks like the computer won this time.");
                                    break;
                                case "o":
                                    setStatus("Wow! Well done! You figured out how to win the unwinnable!");
                                    break;
                                case "-":
                                    setStatus("All right, we'll call it a draw.");
                                    break;
                                default:
                            }

                            // update the tile displays
                            var board = data.game.board,
                                boardLength = board.length;
                            console.log("board: " + board);

                            for (var i = 0; i < boardLength; i++) {
                                var $tile = $("input[name=tile-" + i + "]");
                                if(board[i] == null) {
                                    $tile.removeClass().addClass("btn btn-info").prop('disabled', false);
                                } else {
                                    $tile.removeClass().addClass("btn btn-" + board[i]).val(board[i].toUpperCase()).prop('disabled', true);
                                }
                            }
                        }
                    },
                    error: function (xhr, err) {
                        setStatus('There was a problem communicating with the server. Please try again.')
                    }
                });
            });
        });

        function setStatus(message) {
            if(message == null) {
                $('#status').html("&nbsp;");
            } else {
                $('#status').html(message);
            }
        }

        return this;
    }
}(jQuery));