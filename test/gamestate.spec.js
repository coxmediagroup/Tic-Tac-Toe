var assert = require("assert");
var GameState = require("../server/gameengine/gamestate")
describe('gamestate', function () {
    it('Should show a win along top row for player 1', function () {
        var gameboard = [
            [1, 1, 1],
            [0, 0, 2],
            [2, 0, 1]
        ];
        assert.equal(1, GameState.IsWinner(gameboard));
    });
    it('Should show a win along bottom row for player 1', function () {
        var gameboard = [
            [1, 0, 1],
            [0, 0, 2],
            [1, 1, 1]
        ];
        assert.equal(1, GameState.IsWinner(gameboard));
    });
    it('Should show a win along middle row for player 2', function () {
        var gameboard = [
            [1, 0, 1],
            [2, 2, 2],
            [2, 0, 1]
        ];
        assert.equal(2, GameState.IsWinner(gameboard));
    });
    it('Should show a draw when no moves left and no winners', function () {
        var gameboard = [
            [1, 2, 1],
            [2, 1, 2],
            [2, 2, 1]
        ];
        assert.equal(3, GameState.IsWinner(gameboard));
    });
    it('Should show no winnders when moves left and no winners', function () {
        var gameboard = [
            [1, 2, 0],
            [0, 1, 2],
            [2, 0, 1]
        ];
        assert.equal(0, GameState.IsWinner(gameboard));
    });
});