var $ = jQuery;

$(document).ready(function(){
    board = new Object();
    $(".square").click(function(){
        // Check to see if the square is free
        if ($(this).html()) {
            alert("That square is taken.");

        // TODO: Make this ask if you're sure about the move first.
        } else {
            readBoard(board, $(this).attr('pos'));
            // If square is free, determine best move
            $.post("/board", { board: board }, function(data){
                repopulateBoard(data);
            });
        }

    });

    function readBoard(board, clickedItem) {
        $('#board .row').each(function() {
            temp = new Array();
            $(this).children().each(function(){
                if ( $(this).attr('pos') === clickedItem ) {
                    temp.push('O');
                } else {
                    temp.push($(this).html());
                }
            });
            board[$(this).attr('id')] = temp;
        });
    }
});
