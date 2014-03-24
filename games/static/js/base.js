// Tic-Tac-Toe app by EPiCOWL
(function(app, $, undefined){
    $(document).ready(function(){

        function nextMove(mark, obj){
            var url = "/games/tic-tac-toe/next/";
            data = {
                "mark": mark,
                "obj": obj
            }
            $.getJSON(url, data, updateGame);
        }

        function updateGame(data){
            var $status = $(".status"),
                pMark = data.player_mark,
                cMark = data.computer_mark,
                message = data.message;

                $("#JS_position-"+pMark[0]).html(pMark[1]);
                
                $status.html("Computer's turn...");
                setTimeout(function(){
                    $("#JS_position-"+cMark[0]).html(cMark[1]);
                    
                    if(message != undefined){            
                        $status.html(message).addClass("inflated");
                        $(".jumbotron").fadeOut();
                        $(".header-link a").text("Play Again");
                    } else {
                        $status.html("Your turn");
                    }
                }, 1500);
        }

        function markClickHandler(){
            $(".game-mark").click(function(){
                var $mark = $(this).data("mark"),
                    $obj = $(".game").data("obj");
                
                // Trigger the next move.
                nextMove($mark, $obj);
            });
        }

        // Init mark click handler.
        markClickHandler();
    });
}(window.app = window.app || {}, jQuery));
