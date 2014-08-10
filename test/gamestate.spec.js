var assert = require("assert");
var GameState = require("../server/gameengine/gamestate")
describe('gamestate', function () {
    it('Should show a win along top row', function () {
        var gameboard = [
            [1, 1, 1],
            [0, 1, 2],
            [2, 0, 1]
        ];
        assert.equal(1, GameState.IsWinner(gameboard));
    });
});