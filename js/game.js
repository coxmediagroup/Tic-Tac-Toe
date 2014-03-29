var Row = Backbone.Collection.extend({
    model: Square,

    /* check if all squares in this row are O's (user should never win, so we dont have to check for X win) */
    allO: function() {
        return this.models.every(function(s) {
            return s.attributes.isX === false;
        });
    }

}, {
    numSquares: 3
});

var Game = Backbone.Model.extend({

    initialize: function() {
        var that = this;
        _.each(this.attributes.rows, function(row) {
            row.on('change', function() {
                var result = that.checkForWinner.call(that);
                alert(result);
            });
        })
    },

    _checkVerticalWinner: function() {
        var anyPass = false;
        for (var i = 0 ; i < Row.numSquares ; i++) {
            anyPass = anyPass || this.attributes.rows.every(function(row) {
                var curSquare = row.at(i);
                return curSquare.attributes.isX === false;
            });
        }

        return anyPass;
    },

    _checkDiagWinner: function() {
        var leftDiagPass = true;
        var rightDiagPass = true;
        for (var i = 0, j = Row.numSquares - 1 ; i < Row.numSquares ; i++, j--) {
            var leftDiagSquare = this.attributes.rows[i].at(i);
            var rightDiagSquare = this.attributes.rows[i].at(j);

            leftDiagPass = leftDiagPass && leftDiagSquare.attributes.isX === false;
            rightDiagPass = rightDiagPass && rightDiagSquare.attributes.isX === false;
        }

        return leftDiagPass || rightDiagPass;
    },

    checkForWinner: function() {
        /* check if we've won horizontally, vertically, or diagonally */
        return this._checkVerticalWinner() || this._checkDiagWinner() || _.some(this.attributes.rows, function(row) {
            return row.allO();
        });
    }
});

(function() {
    var NUM_ROWS = 3;
    var $board = $('.board');
    var rows = [];

    for (var i = 0 ; i < NUM_ROWS ; i++) {
        var r = new Row();
        for (var j = 0 ; j < Row.numSquares ; j++) {
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
        rows.push(r);
    }

    new Game({rows: rows});
})();