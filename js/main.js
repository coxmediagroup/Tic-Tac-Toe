var turn        = true; // true = computer turn
    gamestarted = false; // true = game has started, setting cannot be changed
    first       = true; // true = human wants Xs
    realfirst   = true // true = computer first
    humanmoves  = Array();
    compmoves   = Array();

// wait for everything to load
$(document).ready(function() {
    $( ".square" ).click(function() {
        if (gamestarted) {
            if (turn) {
                addComputerSymbol();
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
            realfirst = false;
        }
        else {
            turn = true;
            realfirst = true;
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
            addComputerSymbol();
        }
    }

    function addComputerSymbol() {
        // if computer went first
        if (realfirst) {
            console.log(humanmoves);
            if (compmoves.length == 0 && humanmoves.length == 0) {
                // tic tac toe board, numbered from top to bottom, left to right
                // top-left = 1, middle-middle = 5, bottom-right = 9
                // first move will always be middle for computer
                compmoves.push(5);
                // if(first) {
                //     $("#middle-middle").addClass('');
                // }
                // else {
                //     $("#middle-middle").addClass('x');
                // }
                
                addComputerSymbolHelper(document.getElementById("middle-middle"));
            }
            else {
                var humanLast = humanmoves[humanmoves.length-1];
                // logic for any possible next move after human
                switch (humanLast) {
                    case 1:
                        if (humanmoves.indexOf(2) == -1) {
                            compmoves.push(2);
                            addComputerSymbolHelper(document.getElementById("top-middle"));
                            
                        }
                        else if (humanmoves.indexOf(4) == -1) {
                            compmoves.push(4);
                            addComputerSymbolHelper(document.getElementById("middle-left"));
                        }
                        break;
                    case 2:
                        if (humanmoves.indexOf(3) == -1) {
                            compmoves.push(3);
                            addComputerSymbolHelper(document.getElementById("top-right"));
                            
                        }
                        else if (humanmoves.indexOf(1) == -1) {
                            compmoves.push(1);
                            addComputerSymbolHelper(document.getElementById("top-left"));
                        }
                        break;
                    case 3:
                        if (humanmoves.indexOf(2) == -1) {
                            compmoves.push(2);
                            addComputerSymbolHelper(document.getElementById("top-middle"));
                            
                        }
                        else if (humanmoves.indexOf(6) == -1) {
                            compmoves.push(6);
                            addComputerSymbolHelper(document.getElementById("middle-right"));
                        }
                        break;
                    case 4:
                        if (humanmoves.indexOf(1) == -1) {
                            compmoves.push(1);
                            addComputerSymbolHelper(document.getElementById("top-left"));
                            
                        }
                        else if (humanmoves.indexOf(7) == -1) {
                            compmoves.push(7);
                            addComputerSymbolHelper(document.getElementById("bottom-left"));
                        }
                        break;
                    // no case 5 because computer always picks middle (5) first
                    // case 5:
                    //     compmoves.push(5);
                    //     $("#middle-middle").addClass('x');
                    //     break;
                    case 6:
                        if (humanmoves.indexOf(3) == -1) {
                            compmoves.push(3);
                            addComputerSymbolHelper(document.getElementById("top-right"));
                            
                        }
                        else if (humanmoves.indexOf(9) == -1) {
                            compmoves.push(9);
                            addComputerSymbolHelper(document.getElementById("bottom-right"));
                        }
                        break;
                    case 7:
                        if (humanmoves.indexOf(8) == -1) {
                            compmoves.push(8);
                            addComputerSymbolHelper(document.getElementById("bottom-middle"));
                            
                        }
                        else if (humanmoves.indexOf(4) == -1) {
                            compmoves.push(4);
                            addComputerSymbolHelper(document.getElementById("middle-left"));
                        }
                        break;
                    case 8:
                        if (humanmoves.indexOf(9) == -1) {
                            compmoves.push(9);
                            addComputerSymbolHelper(document.getElementById("bottom-right"));
                            
                        }
                        else if (humanmoves.indexOf(7) == -1) {
                            compmoves.push(7);
                            addComputerSymbolHelper(document.getElementById("bottom-left"));
                        }
                        break;
                    case 9:
                        if (humanmoves.indexOf(8) == -1) {
                            compmoves.push(8);
                            addComputerSymbolHelper(document.getElementById("bottom-middle"));
                            
                        }
                        else if (humanmoves.indexOf(6) == -1) {
                            compmoves.push(6);
                            addComputerSymbolHelper(document.getElementById("middle-right"));
                        }
                        break;
                }
                 
            }
        }
        else { // computer did not go first

        }
    }

    function addComputerSymbolHelper(e) {
        console.log(e);
        if (first) {
            e.className = e.className + " o";
        }
        else {
            e.className = e.className + " x";
        }
    } 

    function addHumanSymbol(e) {
        if (first) {
            $( e ).addClass("x");
        }
        else {
            $( e ).addClass("o");
        }

        addHumanSymbolHelper(e);
    }

    function addHumanSymbolHelper(e) {
        console.log(e.id);
        switch (e.id) {
            case 'top-left':
                humanmoves.push(1);
                break;
            case 'top-middle':
                humanmoves.push(2);
                break;
            case 'top-right':
                humanmoves.push(3);
                break;
            case 'middle-left':
                humanmoves.push(4);
                break;
            case 'middle-middle':
                humanmoves.push(5);
                break;
            case 'middle-right':
                humanmoves.push(6);
                break;
            case 'bottom-left':
                humanmoves.push(7);
                break;
            case 'bottom-middle':
                humanmoves.push(8);
                break;
            case 'bottom-right':
                humanmoves.push(9);
                break;
        }
        console.log(humanmoves);
    }
});