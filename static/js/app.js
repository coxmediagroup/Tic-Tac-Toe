require(['lib/domReady', 'game'], function(domReady, game) {
    domReady(function() {
        game.board = new game.Game();
    });
});
