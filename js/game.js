var Row = Backbone.Collection.extend({
    model: Square,

    /* check how many squares in this row are O's */
    howManyO: function() {
        var count = 0;
        this.models.forEach(function(square) {
            count += square.attributes.isX === false ? 1 : 0;
        });
        return count;
    },

    /* check if all squares in this row are O's (user should never win, so we dont have to check for X win) */
    allO: function() {
        return this.howManyO() === Row.numSquares;
    }
}, {
    numSquares: 3
});

var Game = Backbone.Model.extend({
    initialize: function() {
        var that = this;
        _.each(this.attributes.rows, function(row) {
            row.on('change:isX', function(model, collection, options) {
                if (model.attributes.dontBubble) {
                    return;
                }
                that.computerMove.call(that);
            });
        });
    },

    /*
    get the center square
     */
    _getCenter: function() {
        var middle = Math.floor(Row.numSquares / 2);
        return this.attributes.rows[middle].at(middle);
    },

    /*
    get the first open corner square
     */
    _getFirstOpenCorner: function() {
        var uL = this.attributes.rows[0].at(0),
            uR = this.attributes.rows[0].at(Row.numSquares - 1),
            lL = this.attributes.rows[Row.numSquares - 1].at(0),
            lR = this.attributes.rows[Row.numSquares - 1].at(Row.numSquares - 1);

        return _.find([uL, uR, lL, lR], function(sq) { return sq.isOpen() });
    },

    /*
    get the column for the given index
    @param col - the index of the column to get
     */
    _getColumn: function(col) {
        var colArray = [];
        this.attributes.rows.map(function(row) {
            colArray.push(row.at(col));
        });
        return colArray
    },

    /*
    get the left diagonal if leftDiag is true, right diagonal otherwise
    @param leftDiag - boolean if true get the diagonal starting from 0,0 otherwise diagonal starting from 0,2
     */
    _getDiagonal: function(leftDiag) {
        var diagonal = [];
        for (var i = 0, j = leftDiag ? 0 : Row.numSquares - 1 ; i < Row.numSquares ; i++, j = leftDiag ? j + 1 : j - 1) {
            var cellVal = this.attributes.rows[i].at(j);
            diagonal.push(cellVal);
        }
        return diagonal;
    },

    /*
    check if two squares are populated by the same mark in a row, return the third square if so
    @param checkX - boolean, if true we check for x's in a row, false means o's
     */
    _twoInRow: function(checkX) {
        var that = this;
        for (var i = 0 ; i < Row.numSquares ; i++) {
            var curRow = this.attributes.rows[i].models,
                curCol = this._getColumn(i),
                leftDiag = this._getDiagonal(true),
                rightDiag = this._getDiagonal(false);
            var rowsWithTwoMarks = [curRow, curCol, leftDiag, rightDiag].filter(function(squares) { return that._howMany(squares, checkX) === 2; });

            /* if there are any rows with two marks, see if the last remaining space is open and - if so - return that square */
            var openSquare = undefined;
            for (var j = 0, len = rowsWithTwoMarks.length ; j < len ; j++) {
                var row = rowsWithTwoMarks[j];
                var openSquares = row.filter(function(square) {
                    return square.isOpen();
                });
                if (openSquares.length > 0) openSquare = openSquares[0];
            }
            if (openSquare) return openSquare;
        }

        return false;
    },

    /*
    abstracted function for checking how many in an array of squares are X if checkX=true or O if checkX=false
    @param squares - an array of Square
    @param checkX - boolean, if true check for X's if false check for O's
     */
    _howMany: function(squares, checkX) {
        var count = 0;

        _.each(squares, function(square) {
            if (checkX) {
                count += square.attributes.isX ? 1 : 0;
            } else {
                count += square.attributes.isX === false ? 1 : 0;
            }
        });

        return count;
    },

    /*
    check how many of a given type of mark exist for a given column number
    @param col - the index of the column to check
    @param checkX - boolean for whether to check X's or O's
     */
    _howManyVertical: function(col, checkX) {
        var column = this._getColumn(col);
        return this._howMany(column, checkX);
    },

    /*
    check how many of a given type of mark exist on a diagonal
    @param checkLeftDiag - boolean for whether to check the left diagonal or the right diagonal
    @param checkX - boolean for whether to check X's or O's
     */
    _howManyDiag: function(checkLeftDiag, checkX) {
        var diagonal = this._getDiagonal(checkLeftDiag);
        return this._howMany(diagonal, checkX);
    },

    _checkVerticalWinner: function() {
        var anyPass = false;
        for (var i = 0 ; i < Row.numSquares ; i++) {
            anyPass |= this._howManyVertical(i, false) === Row.numSquares;
        }

        return anyPass;
    },

    _checkDiagWinner: function() {
        var leftDiagWinner = this._howManyDiag(true, false) === Row.numSquares;
        var rightDiagWinner = this._howManyDiag(false, false) === Row.numSquares;
        return leftDiagWinner || rightDiagWinner;
    },

    checkForWinner: function() {
        /* check if we've won horizontally, vertically, or diagonally */
        var won = this._checkVerticalWinner() || this._checkDiagWinner() || _.some(this.attributes.rows, function(row) {
            return row.allO();
        });
        if (won) {
            alert("O wins");
            this.reset();
        }

        return won;
    },

    reset: function() {
        _.each(this.attributes.rows, function(row) {
            row.forEach(function(square) {
                square.set({isX: undefined, dontBubble: true});
                //nasty hack we have to do so that future events bubble..
                square.set({dontBubble: false});
            });
        });
    },

    /*
    we use the rules list here to build our strategy: http://en.wikipedia.org/wiki/Tic-tac-toe
    */
    computerMove: function() {
        var moveSquare = null;
        var makeMove = function(square) {
            square.set({isX: false, dontBubble: true});
        };

        /* Win */
        moveSquare = this._twoInRow(false);
        if (moveSquare) {
            makeMove(moveSquare);
            this.checkForWinner();
            return;
        }

        /* Block */
        moveSquare = this._twoInRow(true);
        if (moveSquare) {
            makeMove(moveSquare);
            return;
        }

        /* Center */
        moveSquare = this._getCenter();
        if (moveSquare.isOpen()) {
            moveSquare.set({isX: false, dontBubble:true});
            return;
        }

        /* Empty Corner */
        moveSquare = this._getFirstOpenCorner();
        if (moveSquare !== undefined) {
            makeMove(moveSquare);
        }
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