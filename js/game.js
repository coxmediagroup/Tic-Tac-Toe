var Row = Backbone.Collection.extend({
    numSquares: 3,
    model: Square
});

(function() {
    var NUM_ROWS = 3;
    var $board = $('.board');

    for (var i = 0 ; i < NUM_ROWS ; i++) {
        var r = new Row();
        for (var j = 0 ; j < r.numSquares ; j++) {
            var s = new Square();
            var v = new SquareView({
                model: s
            }).render();

            /* add the square to the DOM */
            $board.append(v.$el);
            /* make the square a square by setting its height to its width*/
            v.$el.height(v.$el.width());

            r.add(s);
        }

        $board.append("<br />");
    }
})();