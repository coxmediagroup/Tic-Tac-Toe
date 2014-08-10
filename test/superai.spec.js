var assert = require("assert");
var superAI = require("../server/gameengine/superai")
var gameState = require("../server/gameengine/gamestate")
describe('Pauls super AI', function () {
    it('should pick a winning move', function () {
        var gameboard = [
            [2, 2, 0],
            [0, 0, 0],
            [0, 0, 0]
        ];
        var expectedgameboard = [
            [2, 2, 2],
            [0, 0, 0],
            [0, 0, 0]
        ];
        var updatedGameBoard = superAI.AINextMove(gameboard);
        assert.equal(expectedgameboard[0][2], updatedGameBoard[0][2]);
    });

    it('should pick a draw move', function () {
        var gameboard = [
            [1, 2, 1],
            [2, 2, 1],
            [1, 1, 0]
        ];
        var expectedgameboard = [
            [1, 2, 1],
            [2, 2, 1],
            [1, 1, 2]
        ];
        var updatedGameBoard = superAI.AINextMove(gameboard);
        assert.equal(expectedgameboard[2][2], updatedGameBoard[2][2]);
    });

    it('should pick a 0 move', function () {
        var gameboard = [
            [1, 2, 1],
            [2, 0, 0],
            [1, 0, 0]
        ];
        var updatedGameBoard = superAI.AINextMove(gameboard);
        var nowinner = gameState.IsWinner(updatedGameBoard);
        assert.equal(0, nowinner);
    });
 
});