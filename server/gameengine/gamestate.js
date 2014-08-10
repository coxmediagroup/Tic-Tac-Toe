var GameTypes = require("./gametypes");
var OpenSpaces = require("./openspace");
exports.IsWinner = function (gameBoard) {

    //search row wins
    for (var r = 0; r < gameBoard.length; r++) {
        //foreach row
        var row = gameBoard[r];
        var lastMove = row[0];
        var consecutiveCount = 0;
        for (var c = 0; c < row.length; c++) {
            var currentmove = row[c];
            if(currentmove == 0 && lastMove == 0)
            {
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
    
    if(OpenSpaces.GetOpenSpacesCount(gameBoard) < 1)
    return 3;
    
    
    return 0;
};