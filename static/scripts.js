var $ = jQuery;

$(document).ready(function(){
    board = new Object();
    human_char = 'O';
    computer_char = 'X';
    $(".square").click(function(){
        // Check to see if the square is free
        if ($(this).html()) {
            alert("That square is taken.");

        } else {
            readBoard(board, $(this).attr('pos'));
            // If square is free, determine best move
            $.post("/board", { board: board }, function(data){
                repopulateBoard(data["board"], data["is_winner"]);
            });
        }

    });

    $('#messages button').click(function(){
        resetBoard();
    });

    function resetBoard(){
        squares = $('.square');
        $.each(squares, function(){
            $(this).html('');
        });
        $('#messages').hide();
    }

    function readBoard(board, clickedItem) {
        $('#board .row').each(function() {
            temp = new Array();
            $(this).children().each(function(){
                if ( $(this).attr('pos') === clickedItem ) {
                    temp.push(human_char);
                } else {
                    temp.push($(this).html());
                }
            });
            board[$(this).attr('id')] = temp;
        });
    }

    function repopulateBoard(newBoard, isWinner){
        squares = $('.square');
        filledSquares = 0;
        $.each(squares, function(){
            pos = $(this).attr('pos');
            coords = pos.split(',');
            value = newBoard[coords[0]][coords[1]];
            $(this).html(value);
            if (value != '') {
              filledSquares += 1;
            }
        });
        if (isWinner) {
          $('.alert').alert();
          $('#messages').show();
          $('#messages h2').html('You lost!');
        }
        if (!isWinner && filledSquares == 8) {
          $('.alert').alert();
          $('#messages').show();
          $('#messages h2').html('It\'s a draw!');
        }
    }
});
