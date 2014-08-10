var assert = require("assert");
var searcher = require("../server/gameengine/searcher"); 
describe('movesearcher', function () {
    describe('Search', function () {
        it('should find two posible moves', function () {});
        var gameboard = [
            [1, 2, 1],
            [0, 0, 2],
            [2, 0, 1]
        ];
        assert.equal(3, searcher.Search(gameboard));
    });
});