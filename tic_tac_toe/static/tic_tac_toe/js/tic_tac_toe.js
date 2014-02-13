function ViewModel() {
    // Data
    var self = this;
    self.player = "X";
    self.ai = "O";
    self.not_player_turn = ko.observable(true);
    self.squares = [
        ko.observable(''), ko.observable(''), ko.observable(''),
        ko.observable(''), ko.observable(''), ko.observable(''),
        ko.observable(''), ko.observable(''), ko.observable('')
    ];

    self.make_move = function (index) {
        if (!self.not_player_turn() && self.squares[index()]() == "") {
            self.squares[index()](self.player);
            self.reset_ai_message();
            self.not_player_turn(true);

            var temp_squares = Array();
            // Use values in DOM to detect if player is trying to cheat
            for (var index = 0; index < 9; index++) {
                value = $( $(tic_tac_toe).children()[index] ).text();
                if (value != self.squares[index]() || value != "X" || value != "O") {
                    self.end_cheat();
                }
                temp_squares.push(value);
            };

            $.ajax({
                type: 'POST',
                url: $("#tic_tac_toe").attr("data-process-url"),
                data: {
                    "squares": JSON.stringify(temp_squares)
                },
                success: function (data) {
                    if (data.success) {
                        if (data.move_index != -1) {
                            self.squares[data.move_index](self.ai);
                        }
                        self.not_player_turn(false);
                    }
                    else if (data.error = -1) {
                        self.end_cheat();
                    }
                    else {
                        self.end_broke();
                    }
                },
                error: function (data) {
                    self.end_broke();
                }
            });
        }
    };

    self.new_game = function () {
        self.not_player_turn(true);
        $("#turn .not_turn").text("Restarting...");
        $.ajax({
            type: 'POST',
            url: $("#tic_tac_toe").attr("data-new-url"),
            success: function (data) {
                $.each(self.squares, function (index, value) {
                    value("");
                });
                self.not_player_turn(false);
                self.reset_ai_message();
            },
            error: function (data) {
                location.reload();
            }
        });
    }

    self.end_cheat = function () {
        $("#turn .not_turn").text("You cheated. Game Over.");
        self.not_player_turn(true);
    }

    self.end_broke = function () {
        $("#turn .not_turn").text("It Broke. :( Make a New Game.");
        self.not_player_turn(true);
    }

    self.reset_ai_message = function () {
        $("#turn .not_turn").text("Computer is Making Their Turn...");
    }

    setTimeout(function () {
        self.not_player_turn(false);
    }, 2000);
};

ko.bindingHandlers.text_two_way = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        //handle the field changing
        $(element).on("change", function() {
            var observable = valueAccessor();
            observable($(element).text());
        });

    },
    //update the control when the view model changes
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        $(element).text(value);
    }
};

ko.applyBindings(new ViewModel());