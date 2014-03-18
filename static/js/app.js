require(['lib/domReady', 'gameboard'], function(domReady, GameBoard) {
    domReady(function() {
        var gameBoard = new GameBoard('X');
    });
});
