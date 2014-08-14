var GameTypes = require("./gametypes");

exports.GetOpenSpacesCount = function (gameBoard) {
    var count = 0;
    for (var i = 0; i < gameBoard.length; i++) {

        var row = gameBoard[i];
        for (var c = 0; c < row.length; c++) {
            var col = row[c];
            if (col === 0) count++;
        }
    }
    return count;
};

exports.FindMoves = function (gameBoard) {
    var availiblePositions = [];
    for (var r = 0; r < gameBoard.length; r++) {
        var row = gameBoard[r];
        for (var c = 0; c < row.length; c++) {
            var col = row[c];
            if (col === 0) {
                //it's open
                availiblePositions.push(new GameTypes.MovePosition(r, c));
            }
        }
    }
    return availiblePositions;
};
