var turn        = true; // true = computer turn
    gamestarted = false; // true = game has started, setting cannot be changed
    first       = true; // true = human wants Xs

// wait for everything to load
$(document).ready(function() {
    $( ".square" ).click(function() {
        if (gamestarted) {
            if (turn) {
                addComputerSymbol(this);
                changeTurn();
            }
            else {
                addHumanSymbol(this);
                changeTurn();
            }
        }
    });

    $( "#startgame" ).click(function() {
        if (!gamestarted) {
            gamestarted = true;
        }
        var e = document.getElementById("whofirst");
        var whofirst = e.options[e.selectedIndex].value;
        var f = document.getElementById("xoro");
        var xoro = f.options[f.selectedIndex].value;
        
        // adding setting to the game
        if (whofirst == 1) {
            turn = false;
        }
        else {
            turn = true;
        }
        if (xoro == 1) {
            first = true;
        }
        else {
            first = false;
        }

        // starting the game if computer goes first
        if (turn) {
            document.getElementById("top-left").click();
        }

    });

    function changeTurn() {
        if (turn) {
            turn = false;
        }
        else {
            turn = true;
        }
    }

    function addComputerSymbol(e) {
        
    }

    function addComputerSymbolHelper(e) {
        
    }

    function addHumanSymbol(e) {
        if (first) {
            $( e ).addClass("x");
        }
        else {
            $( e ).addClass("o");
        }
    }
});