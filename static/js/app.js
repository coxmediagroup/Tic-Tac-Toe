require(['lib/domReady', 'gameboard', 'game'], function(domReady, GameBoard, game) {
    domReady(function() {
        game.board = new GameBoard(game.host, game.port);
    });
});
