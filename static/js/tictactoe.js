(function($) {
    Square = Backbone.Model.extend({
        defaults: {
            has_x: false,
            has_o: false,
        }
    });

    Board = Backbone.Collection.extend({
        model: Square
    });

    GameView = Backbone.View.extend({
        round: 1,
        initialize: function() {
            this.render();
        },
        render: function() {
            var template = _.template( $("#game_template").html(), {} );
            this.$el.html( template );
        },
        events: {
            "click td": "play"
        },
        play: function(event) {
            var square = $(event.currentTarget);
            var square_index = square.attr("id").split("-")[1];
            square.html("X");
            this.collection.at(square_index).set("has_x", true);
            // computer moves now.
            var board = this.collection
            var self = this
            $.getJSON("/computer", {
                "board[]": JSON.stringify(board),
                "round": this.round,
                "last_play": square_index
                }, 
                function(data) {
                    if (data.square != null) {
                        var square = $("#square-" + data.square);
                        square.html("O");
                        board.at(data.square).set("has_o", true);
                    }
                    if (data.game_over) {
                        self.undelegateEvents();
                    }
                    if (data.winning_squares) {
                        _.each(data.winning_squares, function(square) {
                            var square = $("#square-" + square);
                            square.addClass("winner");
                        });
                        $("#computer-win").show();
                    }
                    else if (data.game_over) {
                        $("#tie-game").show();
                    }
                    
                }
            )
            this.round++;                
        }
    });
    
    // make 9 empty squares to put on the game_board
    var squares = _.map(_.range(9), function () { return {}; })
    var game_board = new Board(squares);
    var game_view = new GameView({el: $("#board"), collection: game_board});

})(jQuery);