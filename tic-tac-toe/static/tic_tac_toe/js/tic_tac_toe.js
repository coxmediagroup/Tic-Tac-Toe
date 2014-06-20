
var TTTGame = function (handler) {
	
	if (typeof handler === "undefined")
		handler = function () {};
	else if (typeof handler !== "function")
		throw {message: "TypeError: handler must be a function"};
	
    var board_data = [];
    var player_symbol = "O";
    var computer_symbol = "X";
    var status;
    var board_markup = '<table><tbody><tr><td data-id="0"></td><td data-id="1" class="center-column"></td><td data-id="2"></td></tr><tr><td data-id="3" class="middle-row"></td><td data-id="4" class="middle-row center-column"></td><td data-id="5" class="middle-row"></td></tr><tr><td data-id="6"></td><td data-id="7" class="center-column"></td><td data-id="8"></td></tr></tbody></table>';
    
    var call_game_backend = function () {
    	status = "PENDING";
    	handler(status);
        $.ajax({
            type: "POST",
            url: "/games/tic-tac-toe/api/v1/play",
            data: JSON.stringify({board: board_data}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        })
        .done(// redraw on success
            function (resp_data) {
                var the_data = resp_data.data;
                board_data = the_data.board;
                //console.log(resp_data);
                redraw(the_data.status, the_data.winner || null);
            }
         )
        .fail(function () {
        	status = "FAIL";
        	handler(status);
        });
    }
    
    var redraw = function (status_, winner) {
        for (i = 0; i < board_data.length; i += 1) {
        	$cell = $("[data-id='" + i + "']");
        	$cell.html(board_data[i]);
            if (board_data[i] !== null)
            	$cell.addClass("done-cell");
        }
        status = status_;
        handler(status);
    };
    
    var reset_board = function () {
        board_data = [null, null, null, null, null, null, null, null, null];
        $("td").removeClass("user-cell").removeClass("done-cell");
    };

    var make_move = function ($cell) {
        $cell.html(player_symbol);
        call_game_backend();
    };
    
    return {
        start: function(starts_symbol) {
        	status = "INIT";
            handler(status);
            reset_board();
            // the computer starts; call the backend
            if (starts_symbol === computer_symbol)
                call_game_backend();
        },
        draw: function($draw_element) {
            $draw_element.empty();
            $draw_element.html(board_markup);
            $draw_element.click(function (event) {
            	if (status === "PENDING")
            		return;
                var $cell = $(event.target);
                var id = $cell.data("id");
                // is this cell already taken?
                if (board_data[id] === null) {
                    board_data[id] = player_symbol;
                    make_move($cell);
                    $cell.addClass("user-cell").addClass("done-cell");
                }
            });
        },
    }
};

	