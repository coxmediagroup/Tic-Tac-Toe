//If I had time I'd do this with Canvas
function renderBoard(result){
    var gameBoard = JSON.parse(result);
    var boardElement = $('#board');
    boardElement.empty();

    for(var i=0;i<3;i++){
        var row = gameBoard.board[i];
        var rowElement = boardElement.append('<div class="row"></div>');
        for(var j=0;j<3;j++){
            var cellValue = row[j];
            rowElement.append('<span class="column" onclick="makeMove(' + i + ',' + j + ');">' + cellValue + '</span>');
        }
    }

    checkWin();
}

function getBoard(){
    $.get("/api/board", function(result) {
        renderBoard(result);
    });
}

function makeMove(x, y){
    var url = '/api/makemove?x=' + x + "&y=" + y;
    $.get(url, function(result){
        renderBoard(result);
    });
}

function newGame(){
    $.get("/api/newgame", function(result){
        renderBoard(result);
    });
}

function checkWin(){
    $.get("/api/checkwin", function(result){
        $('#announcement').html(result);
    })
}