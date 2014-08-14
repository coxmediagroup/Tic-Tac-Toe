var assert = require("assert");
var openSpace = require("../server/gameengine/openspace");
var GameTypes = require("../server/gameengine/gametypes");

describe('openSpace', function () {
    describe('GetOpenSpacesCount', function () {
        it('should return 2 open spaces', function () {
            var gameboard = [
                [1, 2, 1],
                [0, 1, 2],
                [2, 0, 1]
            ];
            assert.equal(2, openSpace.GetOpenSpacesCount(gameboard));
            assert.notEqual(1, openSpace.GetOpenSpacesCount(gameboard));
        });
        it('should return 5 open spaces', function () {
            var gameboard = [
                [0, 2, 1],
                [0, 0, 2],
                [2, 0, 0]
            ];
            assert.equal(5, openSpace.GetOpenSpacesCount(gameboard));
            assert.notEqual(3, openSpace.GetOpenSpacesCount(gameboard));
        });
        it('should return 0 open spaces', function () {
            var gameboard = [
                [1, 2, 1],
                [1, 1, 2],
                [2, 2, 1]
            ];
            assert.equal(0, openSpace.GetOpenSpacesCount(gameboard));
            assert.notEqual(5, openSpace.GetOpenSpacesCount(gameboard));
        });
    });
    describe('GetOpenLocations', function () {
        it('should find a move at row 0 col 1', function () {
            var gameboard = [
                [1, 0, 1],
                [1, 1, 2],
                [2, 1, 2]
            ];
            var expected = new GameTypes.MovePosition(0, 1);
            var actual = openSpace.FindMoves(gameboard);
            assert.equal(expected.column, actual[0].column);
            assert.equal(expected.row, actual[0].row);
            assert.equal(1, actual.length);
        });
        it('should find open moves at row 0 col 2 and row 2 col 1', function () {
            var gameboard = [
                [1, 0, 1],
                [1, 1, 2],
                [2, 2, 0]
            ];
            var expected = [new GameTypes.MovePosition(0, 2), new GameTypes.MovePosition(2, 1)];
            var actual = openSpace.FindMoves(gameboard);
            assert.equal(expected.length, actual.length);

            assert.equal(expected[0].col, actual[0].col);
            assert.equal(expected[0].row, actual[0].row);

            assert.equal(expected[1].col, actual[1].col);
            assert.equal(expected[1].row, actual[1].row);

        });
    });
});