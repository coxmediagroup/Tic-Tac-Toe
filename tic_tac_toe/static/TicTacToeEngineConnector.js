var TicTacToeEngineConnector = {
    disconnectClickListeners: function () {
        $("[id^=section]").off("click");
    },

    connectClickListeners: function () {
        // Add listeners for click actions onto game squares.
        // I'm sure there is a non-redundant way to do this.
        $("#section_1").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(1);
        });
        $("#section_2").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(2);
        });
        $("#section_3").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(3);
        });
        $("#section_4").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(4);
        });
        $("#section_5").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(5);
        });
        $("#section_6").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(6);
        });
        $("#section_7").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(7);
        });
        $("#section_8").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(8);
        });
        $("#section_9").on("click", function () {
            TicTacToeEngineConnector.respondToPlayerMove(9);
        });
    },

    respondToPlayerMove: function (squareId) {
        $.ajax({
            // the URL for the request
            url: "/tic_tac_toe/process-player-move/",

            // the data to send (will be converted to a query string)
            data: {
                id: squareId
            },

            // whether this is a POST or GET request
            type: "POST",

            // the type of data we expect back
            dataType: "json",

            // code to run if the request succeeds;
            // the response is passed to the function
            success: function (json) {
                if (json.error_message) {
                    $("#error_message").text(json.error_message);
                    $("#error_message").slideDown();
                } else {
                    $("#error_message").slideUp();
                    $("#section_" + json.player_move).addClass("player_selected");
                    $("#section_" + json.computer_move).addClass("computer_selected");

                    switch (json.game_status) {
                        case "Draw":
                            $("#status_message").find("h3").text("// TIE GAME");
                            $("#status_message").find("p").text(
                                "Not bad Whippersnapper!  You " +
                                    "didn't lose.  That's quite an " +
                                    "accomplishment for you.")
                            $("#status_message").slideDown();
                            TicTacToeEngineConnector.disconnectClickListeners();
                            break;
                        case "Game Over (Computer Win)":
                            $("#status_message").find("h3").text("// YOU LOST");
                            $("#status_message").find("p").text(
                                "You win some, you lose some. " +
                                    "Actually, you're never going to win " +
                                    "some.")
                            $("#status_message").slideDown();
                            TicTacToeEngineConnector.disconnectClickListeners();
                        //break;
                    }

                }
            },

            // code to run if the request fails; the raw request and
            // status codes are passed to the function
            error: function (xhr, status) {
                alert("Sorry, there was a problem!");
            },

            // code to run regardless of success or failure
            complete: function (xhr, status) {
                //alert( "The request is complete!" );
            }
        });
    }
};