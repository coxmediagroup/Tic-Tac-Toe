var openSpace = require("./openspace");
var gameState = require("./gamestate");
var gameTypes = require("./gametypes");

exports.AINextMove = function (gameBoard) {
    var posibleMoves = openSpace.FindMoves(gameBoard);

    for (var move = 0; move < posibleMoves.length; move++) {
        var tempboard =  JSON.parse(JSON.stringify(gameBoard));
        var position = posibleMoves[move];

        tempboard[position.row][position.column] = 2;
        var result = gameState.IsWinner(tempboard);
        if (result === 2) {
            return tempboard;
        } 
    }
    //if all winning options are exausted next best is 0 no winner yet or draw
    for (var move = 0; move < posibleMoves.length; move++) {
        var tempboard = JSON.parse(JSON.stringify(gameBoard));
        var position = posibleMoves[move];

        tempboard[position.row][position.column] = 2;
        var result = gameState.IsWinner(tempboard);
        if (result === 0 || result === 3) {
            return tempboard;
        } 
    }
     
    return gameBoard;
}