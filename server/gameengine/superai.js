var openSpace = require("./openspace");
var gameState = require("./gamestate");
var gameTypes = require("./gametypes");

exports.AINextMove = function (gameBoard) {
    var posibleMoves = openSpace.FindMoves(gameBoard);


    var result = BlockOponent(gameBoard);
    if (result.status === 1) {
        return result.gameBoard;
    }
    result = GetMyWinningMove(gameBoard);
    if (result.status === 1) {
        return result.gameBoard;
    }
    result = GetDrawOrNoWinner(gameBoard);
    if (result.status === 1) {
        return result.gameBoard;
    }



    return gameBoard;
}

function BlockOponent(gameBoard) {
    var posibleMoves = openSpace.FindMoves(gameBoard);
    var status = 0;
    //first block oponent moves
    for (var move = 0; move < posibleMoves.length; move++) {
        var tempboard = JSON.parse(JSON.stringify(gameBoard));
        var position = posibleMoves[move];

        tempboard[position.row][position.column] = 1;
        var result = gameState.IsWinner(tempboard);
        if (result === 1) {
            //this move would result in player 1 winning
            //block!!!
            tempboard[position.row][position.column] = 2;
            return {
                gameBoard: tempboard,
                status: 1
            };
        }
    }
    return {
        gameBoard: gameBoard,
        status: 0
    }
}

function GetMyWinningMove(gameBoard) {
    var posibleMoves = openSpace.FindMoves(gameBoard);
    for (var move = 0; move < posibleMoves.length; move++) {
        var tempboard = JSON.parse(JSON.stringify(gameBoard));
        var position = posibleMoves[move];

        tempboard[position.row][position.column] = 2;
        var result = gameState.IsWinner(tempboard);
        if (result === 2) {
            return {
                gameBoard: tempboard,
                status: 1
            };
        }
    }
    return {
        gameBoard: gameBoard,
        status: 0
    }
}

function GetDrawOrNoWinner(gameBoard) {
    var posibleMoves = openSpace.FindMoves(gameBoard);
    //if all winning options are exausted next best is 0 no winner yet or draw
    for (var move = 0; move < posibleMoves.length; move++) {
        var tempboard = JSON.parse(JSON.stringify(gameBoard));
        var position = posibleMoves[move];

        tempboard[position.row][position.column] = 2;
        var result = gameState.IsWinner(tempboard);
        if (result === 0 || result === 3) {
            return {
                gameBoard: tempboard,
                status: 1
            };
        }
    }
    return {
        gameBoard: gameBoard,
        status: 0
    }
}