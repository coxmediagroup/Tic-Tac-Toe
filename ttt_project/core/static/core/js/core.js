$(function() {
    $('input[name="username"]').focus();

    $('#game_board td').click(function(el) {
        space_id = this.id;
        game_id = $('#header span').text();
        // alert('clicked on space ' + game_id);

        $.ajax({
            type: "GET",
            url: "/player_move/"+game_id+"/"+space_id+"/",
            dataType: "html",
            success: function(data) {
                if (data == "True") {
                    // alert("Move Saved for space: " + space_id);
                }
                $("#game_board").replaceWith(data);
            }
        });
    });
});
