function setUpGame(url, playerLetter){
    $('#board-space').on("click", "ul li img.empty",function(){
        var idStr =  $(this).attr('id');
        var id = parseInt(idStr[4]);
        board[id] = playerLetter;
        console.log(id);
        console.log(board);
        var boardJson = JSON.stringify(board);
        $.post(url, {"board_json": boardJson}, replaceBoard);
    });
}

function replaceBoard(board_html){
    console.log(board_html);
    $("#board-space").html(board_html);
}