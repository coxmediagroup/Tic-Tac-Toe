(function($) {
    Square = Backbone.Model.extend({
        defaults: {
            has_x: false,
            has_o: false
        }
    });

    Board = Backbone.Collection.extend({
        model: Square
    });

    GameView = Backbone.View.extend({
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
            var square_el = $(event.currentTarget);
            var square_index = square_el.attr("id").split("-")[1];
            var square = this.collection.at(square_index);
            if (!square.get("has_x") && !square.get("has_o")) {
                square_el.html("X");
                square.set("has_x", true);
                this.computer_move();
            }
        },
        computer_move: function() {
            var board = this.collection
            var self = this
            $.getJSON("/computer", {
                "board[]": JSON.stringify(board)
                }, 
                function(data) {
                    if (data.square != null) {
                        var square = $("#square-" + data.square);
                        square.html("O").fadeIn("slow");
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
                        self.$el.find("td").addClass("tie");
                    }
                    
                }
            )
        }
    });
    
    // make 9 empty squares to put on the game_board
    var squares = _.map(_.range(9), function () { return {}; })
    var game_board = new Board(squares);
    var game_view = new GameView({el: $("#board"), collection: game_board});

})(jQuery);