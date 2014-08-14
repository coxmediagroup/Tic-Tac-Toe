var superAI = require("../gameengine/superai");
var gameState = require("../gameengine/gamestate");
exports.makeMove = function (req, res) {
    var gameBoard = req.body;
    var winner = 0;
    //first check to see if player 1 won already
    var preState = GetGameResult(gameBoard);
    if (preState !== 0) {
        res.json({
            winner: preState,
            gameBoard: gameBoard
        });
    }

    //make ai move if no winners
    var airesult = superAI.AINextMove(gameBoard);

    var postState = GetGameResult(airesult);

    res.json({
        winner: postState,
        gameBoard: airesult
    });

};

function GetGameResult(gameBoard) {
    var state = gameState.IsWinner(gameBoard);
    return state;
}
 