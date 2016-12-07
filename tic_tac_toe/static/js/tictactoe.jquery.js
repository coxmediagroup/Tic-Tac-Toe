(function($) {
    /**
     * Handles passing plays to server and updating game state.
     * Works on DOM form node with child node ids of form "X_Y".
     */
    $.fn.ticTacToe = function() {
        // Handle submitting a particular input and updating the dom with new
        // game state.
        var url = $(this).attr('action');
        var doSubmit = function(command) {
            var data = {};
            data[command] = command;
            $.post(url, data, function(response) {
                // Update the gameboard with each position.
                $.each(response.positions, function(name, value) {
                    if (value) {
                        $('#' + name).val(value).attr('disabled', true);
                    }
                    else {
                        $('#' + name).val('').attr('disabled', response.gameover);
                    }
                });

                // Update status and reset button.
                $('#status-message').html(response.status);
                if (response.gameover) {
                    $('#replay-button').show(500);
                }
                else {
                    $('#replay-button').hide(500);
                }
            });
            return false;
        };

        // Bind a submit handler to this node to override standard form
        // submission.
        // Use click handler so we can determine which input was used
        // to submit form.
        $.each($(this).find(':submit'), function() {
            $(this).click(function() {
                doSubmit($(this).attr('name'));
            });
        });

        // Disable normal form submission; use above click handler instead.
        $(this).submit(function() {
              return false;
        });

        return this;
    };
})(jQuery);
