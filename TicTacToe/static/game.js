
function getBoardState() {
    var board = [[' ', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']];
    $("#tictactoe a").each(function() {
        var rowcol = $(this).attr("id");
        if ($(this).hasClass('xchoice')) {
            board[parseInt(rowcol[1])][parseInt(rowcol[2])] = 'X';
        }
        else if ($(this).hasClass('ochoice')) {
            board[parseInt(rowcol[1])][parseInt(rowcol[2])] = 'O';
        }
    });
    return board;
}

function updateBoardState(json) {
    var winner = json.winner;
    var board = json.board;
    for (var i in board) {
        for (var j in board[i]) {
            if (board[i][j] == 'X') {
                $("#c" + i + j).removeClass('ochoice').removeClass('empty').addClass('xchoice');
            }
            else if (board[i][j] == 'O') {
                $("#c" + i + j).removeClass('empty').removeClass('xchoice').addClass('ochoice');
            }
            else {
                $("#c" + i + j).removeClass('ochoice').removeClass('xchoice').addClass('empty');
            }
        }
    }
    if (winner) {
        $(".empty").removeClass('empty');
    }
}

$(document).ready(function() {
    $(".empty").live('click', function() {
        $(this).removeClass('empty').addClass('xchoice');
        $.ajax({
            type: 'POST',
            url: '/',
            data: {board: JSON.stringify(getBoardState())},
            success: function(json) {
                updateBoardState(json);
            }
        });
    });
    $("#rttt").click(function(evt) {
        window.location.reload();
        evt.stopPropagation();
        evt.preventDefault();
    });
});
