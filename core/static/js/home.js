(function($) {
    "use strict";

    $(".play-first").click(function(event){
        window.location.assign("/tictactoe?order=first");
    });

    $(".play-second").click(function(event){
        window.location.assign("/tictactoe?order=second");
    });

}(jQuery));

