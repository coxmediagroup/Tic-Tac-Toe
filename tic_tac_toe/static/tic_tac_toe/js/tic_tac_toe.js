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
                if (value != self.squares[index]() || (value != "X" && value != "O" && value != "")) {
                    self.end_cheat();
                }
                temp_squares.push(value);
            };

            if (self.check_win(self.player)) {
                self.end_win();
            }
            else if (self.check_tie()) {
                self.end_tie();
            }
            else {
                $.ajax({
                    type: 'POST',
                    url: $("#tic_tac_toe").attr("data-process-url"),
                    data: {
                        "squares": JSON.stringify(temp_squares),
                        "ai": self.ai
                    },
                    success: function (data) {
                        if (data.success) {
                            if (data.move_index != -1) {
                                self.squares[data.move_index](self.ai);
                            }
                            if (self.check_win(self.ai)) {
                                self.end_lose();
                            }
                            else {
                                self.not_player_turn(false);
                            }
                        }
                        else if (data.error == -1) {
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

    self.check_win = function (side) {
        //0, 1, 2  ||  X, X, X 
        //3, 4, 5  ||  X, 4, 5
        //6, 7, 8  ||  6, 7, 8

        // check 0
        if (self.squares[0]() == side) {
            if (self.squares[1]() == side) {
                if (self.squares[2]() == side) {
                    return true;
                }
            }
            if (self.squares[3]() == side) {
                if (self.squares[6]() == side) {
                    return true;
                }
            }
            if (self.squares[4]() == side) {
                if (self.squares[8]() == side) {
                    return true;
                }
            }
        }
        // check 1
        if (self.squares[1]() == side) {
            if (self.squares[4]() == side) {
                if (self.squares[7]() == side) {
                    return true;
                }
            }
        }
        // check 2
        if (self.squares[2]() == side) {
            if (self.squares[4]() == side) {
                if (self.squares[6]() == side) {
                    return true;
                }
            }
            if (self.squares[5]() == side) {
                if (self.squares[8]() == side) {
                    return true;
                }
            }
        }
        // check 3
        if (self.squares[3]() == side) {
            if (self.squares[4]() == side) {
                if (self.squares[5]() == side) {
                    return true;
                }
            }
        }
        // check 6
        if (self.squares[6]() == side) {
            if (self.squares[7]() == side) {
                if (self.squares[8]() == side) {
                    return true;
                }
            }
        }
        // no need to check rest

        return false;
    }

    self.check_tie = function () {
        for (var index = 0; index < 9; index++) {
            if (self.squares[index]() == "") {
                return false;
            }
        }
        return true;
    }

    // cheat detection is not nearly perfect :( Good start though
    self.end_cheat = function () {
        $("#turn .not_turn").text("You cheated. Game Over.");
        self.not_player_turn(true);
    }

    self.end_broke = function () {
        $("#turn .not_turn").text("It Broke. :( Make a New Game.");
        self.not_player_turn(true);
    }

    self.end_win = function () {
        $("#turn .not_turn").text("You won!");
        self.not_player_turn(true);
    }

    self.end_lose = function () {
        $("#turn .not_turn").text("Oh, darn. You lost. :(");
        self.not_player_turn(true);
    }

    self.end_tie = function () {
        $("#turn .not_turn").text("Cat won. :/");
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
