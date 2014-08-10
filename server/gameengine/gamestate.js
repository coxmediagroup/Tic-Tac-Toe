var GameTypes = require("./gametypes");
var OpenSpaces = require("./openspace");
exports.IsWinner = function (gameBoard) {

    //search row wins
    var rowresult = RowWinTester(gameBoard);
    if (rowresult !== 0) return rowresult;

    var colresult = ColWinTester(gameBoard);
    if (colresult !== 0) return colresult;

    var diagresult = DiagWinTester(gameBoard);
    if (diagresult !== 0) return diagresult;

    if (OpenSpaces.GetOpenSpacesCount(gameBoard) < 1) return 3;


    return 0;
};




var RowWinTester = function (gameBoard) {
    for (var r = 0; r < gameBoard.length; r++) {
        //foreach row
        var row = gameBoard[r];
        var lastMove = row[0];
        var consecutiveCount = 0;
        for (var c = 0; c < row.length; c++) {
            var currentmove = row[c];
            if (currentmove === 0 && lastMove === 0) {
                consecutiveCount = 0;
                continue;
            }
            if (currentmove != lastMove) {
                consecutiveCount = 0;
                continue;
            }
            else consecutiveCount++;
        }
        if (consecutiveCount === 3) return lastMove;
    }
    return 0;
};

var ColWinTester = function (gameBoard) {

    //TODO hardcoded height to 3 make dynamic for bigger boards
    for (var c = 0; c < gameBoard.length; c++) {
        //iterate down columns rather than rows
        var lastMove = gameBoard[0][c]; //always start at row 0 and move down
        var consecutiveCount = 0;
        for (var r = 0; r < gameBoard.length; r++) {
            var currentmove = gameBoard[r][c];

            if (currentmove === 0 && lastMove === 0) {
                consecutiveCount = 0;
                continue;
            }

            if (currentmove != lastMove) {
                consecutiveCount = 0;
                continue;
            }
            else consecutiveCount++;


        }
        if (consecutiveCount === 3) return lastMove;
    }

    return 0;
};

var DiagWinTester = function (gameBoard) {
    //1,0,0
    //0,1,0
    //0,0,1
    //each row change starts the search col out last c + 1
    for (var r = 0; r < gameBoard.length; r++) {
        var row = gameBoard[r];
        var lastcol = 0;
        for (var c = 0; c < row.length; r++) {
 
        }

    }



    return 0;
};

exports.ColWinTester;
exports.RowWinTester;
