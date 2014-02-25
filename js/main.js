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
            changeTurn();
        }
    }

    function addComputerSymbol() {
        var humanLast = humanmoves[humanmoves.length-1];
        
        console.log("adding computer symbol");
        console.log(compmoves);
        // if computer went first
        if (realfirst) {
            //console.log(humanmoves);
            if (compmoves.length == 0 && humanmoves.length == 0) {
                // tic tac toe board, numbered from top to bottom, left to right
                // top-left = 1, middle-middle = 5, bottom-right = 9
                // first move will always be middle for computer
                compmoves.push(5);
                
                addComputerSymbolHelper(document.getElementById("middle-middle"));
            }
            else {
                // logic for any possible next move after computer first mover and human 1st move
                console.log("did i win");
                var canWin = computerCanWin();
                console.log(canWin);
                if (canWin > 0) {
                    console.log("can win");
                    switch (canWin) {
                        case 1:
                            addComputerSymbolHelper(document.getElementById("top-left"));
                            break;
                        case 2:
                            addComputerSymbolHelper(document.getElementById("top-middle"));
                            break;
                        case 3:
                            addComputerSymbolHelper(document.getElementById("top-right"));
                            break;
                        case 4:
                            addComputerSymbolHelper(document.getElementById("middle-left"));
                            break;
                        case 5:
                            addComputerSymbolHelper(document.getElementById("middle-middle"));
                            break;
                        case 6:
                            addComputerSymbolHelper(document.getElementById("middle-right"));
                            break;
                        case 7:
                            addComputerSymbolHelper(document.getElementById("bottom-left"));
                            break;
                        case 8:
                            addComputerSymbolHelper(document.getElementById("bottom-middle"));
                            break;
                        case 9:
                            addComputerSymbolHelper(document.getElementById("bottom-right"));
                            break;
                    }
                }
                else {
                    console.log("cant win yet");
                    console.log("humanmoves");
                    console.log(humanmoves);
                    switch (humanLast) {
                        case 1:
                            if (humanmoves.indexOf(2) == -1 &&  compmoves.indexOf(2) == -1) {
                                compmoves.push(2);
                                addComputerSymbolHelper(document.getElementById("top-middle"));
                                
                            }
                            else if (humanmoves.indexOf(4) == -1 &&  compmoves.indexOf(4) == -1) {
                                compmoves.push(4);
                                addComputerSymbolHelper(document.getElementById("middle-left"));
                            }
                            break;
                        case 2:
                            if (humanmoves.indexOf(3) == -1 &&  compmoves.indexOf(3) == -1) {
                                compmoves.push(3);
                                addComputerSymbolHelper(document.getElementById("top-right"));
                                
                            }
                            else if (humanmoves.indexOf(1) == -1 &&  compmoves.indexOf(1) == -1) {
                                compmoves.push(1);
                                addComputerSymbolHelper(document.getElementById("top-left"));
                            }
                            break;
                        case 3:
                            if (humanmoves.indexOf(2) == -1 &&  compmoves.indexOf(2) == -1) {
                                compmoves.push(2);
                                addComputerSymbolHelper(document.getElementById("top-middle"));
                                
                            }
                            else if (humanmoves.indexOf(6) == -1 &&  compmoves.indexOf(6) == -1) {
                                compmoves.push(6);
                                addComputerSymbolHelper(document.getElementById("middle-right"));
                            }
                            break;
                        case 4:
                            if (humanmoves.indexOf(1) == -1 &&  compmoves.indexOf(1) == -1) {
                                compmoves.push(1);
                                addComputerSymbolHelper(document.getElementById("top-left"));
                                
                            }
                            else if (humanmoves.indexOf(7) == -1 &&  compmoves.indexOf(7) == -1) {
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
                            if (humanmoves.indexOf(3) == -1 &&  compmoves.indexOf(3) == -1) {
                                compmoves.push(3);
                                addComputerSymbolHelper(document.getElementById("top-right"));
                                
                            }
                            else if (humanmoves.indexOf(9) == -1 &&  compmoves.indexOf(9) == -1) {
                                compmoves.push(9);
                                addComputerSymbolHelper(document.getElementById("bottom-right"));
                            }
                            break;
                        case 7:
                            if (humanmoves.indexOf(8) == -1 &&  compmoves.indexOf(8) == -1) {
                                compmoves.push(8);
                                addComputerSymbolHelper(document.getElementById("bottom-middle"));
                                
                            }
                            else if (humanmoves.indexOf(4) == -1 &&  compmoves.indexOf(4) == -1) {
                                compmoves.push(4);
                                addComputerSymbolHelper(document.getElementById("middle-left"));
                            }
                            break;
                        case 8:
                            if (humanmoves.indexOf(9) == -1 &&  compmoves.indexOf(9) == -1) {
                                compmoves.push(9);
                                addComputerSymbolHelper(document.getElementById("bottom-right"));
                                
                            }
                            else if (humanmoves.indexOf(7) == -1 &&  compmoves.indexOf(7) == -1) {
                                compmoves.push(7);
                                addComputerSymbolHelper(document.getElementById("bottom-left"));
                            }
                            break;
                        case 9:
                            if (humanmoves.indexOf(8) == -1 && compmoves.indexOf(8) == -1) {
                                compmoves.push(8);
                                addComputerSymbolHelper(document.getElementById("bottom-middle"));
                                
                            }
                            else if (humanmoves.indexOf(6) == -1 &&  compmoves.indexOf(6) == -1) {
                                compmoves.push(6);
                                addComputerSymbolHelper(document.getElementById("middle-right"));
                            }
                            break;
                    }
                }
                
                 
            }
        }
        else { // computer did not go first
            // logic for any possible next move after human first move
            console.log("did i win");
            var canWin = computerCanWin();
            console.log(canWin);
            if (canWin > 0) {
                console.log("can win");
                switch (canWin) {
                    case 1:
                        addComputerSymbolHelper(document.getElementById("top-left"));
                        break;
                    case 2:
                        addComputerSymbolHelper(document.getElementById("top-middle"));
                        break;
                    case 3:
                        addComputerSymbolHelper(document.getElementById("top-right"));
                        break;
                    case 4:
                        addComputerSymbolHelper(document.getElementById("middle-left"));
                        break;
                    case 5:
                        addComputerSymbolHelper(document.getElementById("middle-middle"));
                        break;
                    case 6:
                        addComputerSymbolHelper(document.getElementById("middle-right"));
                        break;
                    case 7:
                        addComputerSymbolHelper(document.getElementById("bottom-left"));
                        break;
                    case 8:
                        addComputerSymbolHelper(document.getElementById("bottom-middle"));
                        break;
                    case 9:
                        addComputerSymbolHelper(document.getElementById("bottom-right"));
                        break;
                }
            }
            else {
                console.log("cant win yet");
                console.log("humanmoves");
                console.log(humanmoves);
                console.log("compmoves");
                console.log(compmoves);
                console.log("can human win");
                var canHumanWin = humanCanWin();
                console.log(canHumanWin);
                // have to block human if he/she can win
                if (canHumanWin > 0) {
                    console.log("human can win");
                    switch (canHumanWin) {
                        case 1:
                            addComputerSymbolHelper(document.getElementById("top-left"));
                            compmoves.push(1);
                            break;
                        case 2:
                            addComputerSymbolHelper(document.getElementById("top-middle"));
                            compmoves.push(2);
                            break;
                        case 3:
                            addComputerSymbolHelper(document.getElementById("top-right"));
                            compmoves.push(3);
                            break;
                        case 4:
                            addComputerSymbolHelper(document.getElementById("middle-left"));
                            compmoves.push(4);
                            break;
                        case 5:
                            addComputerSymbolHelper(document.getElementById("middle-middle"));
                            compmoves.push(5);
                            break;
                        case 6:
                            addComputerSymbolHelper(document.getElementById("middle-right"));
                            compmoves.push(6);
                            break;
                        case 7:
                            addComputerSymbolHelper(document.getElementById("bottom-left"));
                            compmoves.push(7);
                            break;
                        case 8:
                            addComputerSymbolHelper(document.getElementById("bottom-middle"));
                            compmoves.push(8);
                            break;
                        case 9:
                            addComputerSymbolHelper(document.getElementById("bottom-right"));
                            compmoves.push(9);
                            break;
                    }
                }
                else {
                    switch (humanLast) {
                        case 1:
                            if (humanmoves.indexOf(2) == -1 &&  compmoves.indexOf(2) == -1) {
                                compmoves.push(2);
                                addComputerSymbolHelper(document.getElementById("top-middle"));
                                
                            }
                            else if (humanmoves.indexOf(4) == -1 &&  compmoves.indexOf(4) == -1) {
                                compmoves.push(4);
                                addComputerSymbolHelper(document.getElementById("middle-left"));
                            }
                            break;
                        case 2:
                            if (humanmoves.indexOf(3) == -1 &&  compmoves.indexOf(3) == -1) {
                                compmoves.push(3);
                                addComputerSymbolHelper(document.getElementById("top-right"));
                                
                            }
                            else if (humanmoves.indexOf(1) == -1 &&  compmoves.indexOf(1) == -1) {
                                compmoves.push(1);
                                addComputerSymbolHelper(document.getElementById("top-left"));
                            }
                            break;
                        case 3:
                            if (humanmoves.indexOf(2) == -1 &&  compmoves.indexOf(2) == -1) {
                                compmoves.push(2);
                                addComputerSymbolHelper(document.getElementById("top-middle"));
                                
                            }
                            else if (humanmoves.indexOf(6) == -1 &&  compmoves.indexOf(6) == -1) {
                                compmoves.push(6);
                                addComputerSymbolHelper(document.getElementById("middle-right"));
                            }
                            break;
                        case 4:
                            if (humanmoves.indexOf(1) == -1 &&  compmoves.indexOf(1) == -1) {
                                compmoves.push(1);
                                addComputerSymbolHelper(document.getElementById("top-left"));
                                
                            }
                            else if (humanmoves.indexOf(7) == -1 &&  compmoves.indexOf(7) == -1) {
                                compmoves.push(7);
                                addComputerSymbolHelper(document.getElementById("bottom-left"));
                            }
                            break;
                        case 5:
                            if (humanmoves.indexOf(1) == -1 &&  compmoves.indexOf(1) == -1) {
                                compmoves.push(1);
                                addComputerSymbolHelper(document.getElementById("top-left"));
                                
                            }
                            break;
                        case 6:
                            if (humanmoves.indexOf(3) == -1 &&  compmoves.indexOf(3) == -1) {
                                compmoves.push(3);
                                addComputerSymbolHelper(document.getElementById("top-right"));
                                
                            }
                            else if (humanmoves.indexOf(9) == -1 &&  compmoves.indexOf(9) == -1) {
                                compmoves.push(9);
                                addComputerSymbolHelper(document.getElementById("bottom-right"));
                            }
                            break;
                        case 7:
                            if (humanmoves.indexOf(8) == -1 &&  compmoves.indexOf(8) == -1) {
                                compmoves.push(8);
                                addComputerSymbolHelper(document.getElementById("bottom-middle"));
                                
                            }
                            else if (humanmoves.indexOf(4) == -1 &&  compmoves.indexOf(4) == -1) {
                                compmoves.push(4);
                                addComputerSymbolHelper(document.getElementById("middle-left"));
                            }
                            break;
                        case 8:
                            if (humanmoves.indexOf(9) == -1 &&  compmoves.indexOf(9) == -1) {
                                compmoves.push(9);
                                addComputerSymbolHelper(document.getElementById("bottom-right"));
                                
                            }
                            else if (humanmoves.indexOf(7) == -1 &&  compmoves.indexOf(7) == -1) {
                                compmoves.push(7);
                                addComputerSymbolHelper(document.getElementById("bottom-left"));
                            }
                            break;
                        case 9:
                            if (humanmoves.indexOf(8) == -1 && compmoves.indexOf(8) == -1) {
                                compmoves.push(8);
                                addComputerSymbolHelper(document.getElementById("bottom-middle"));
                                
                            }
                            else if (humanmoves.indexOf(6) == -1 &&  compmoves.indexOf(6) == -1) {
                                compmoves.push(6);
                                addComputerSymbolHelper(document.getElementById("middle-right"));
                            }
                            break;
                    }
                }
            }
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
        console.log("humanmoves");
        console.log(humanmoves);
    }

    function computerCanWin() {
        if (contains(1, compmoves)) {
            if (contains(2, compmoves)) {
                if (!contains(3, humanmoves)) {
                    return computerCanWinHelper(3);
                }
                
            }
            else if (contains(3, compmoves)) {
                if (!contains(2, humanmoves)) {
                    return computerCanWinHelper(2);
                }
                
            }
            else if (contains(4, compmoves)) {
                if (!contains(7, humanmoves)) {
                    return computerCanWinHelper(7);
                }
                
            }
            else if (contains(5, compmoves)) {
                if (!contains(9, humanmoves)) {
                    return computerCanWinHelper(9);
                }
                
            }
            else if (contains(7, compmoves)) {
                if (!contains(4, humanmoves)) {
                    return computerCanWinHelper(4);
                }
                
            }
            else if (contains(9, compmoves)) {
                if (!contains(5, humanmoves)) {
                    return computerCanWinHelper(5);
                }
                
            }
        }
        if (contains(2, compmoves)) {
            if (contains(3, compmoves)) {
                if (!contains(1, humanmoves)) {
                    return computerCanWinHelper(1);
                }
                
            }
            else if (contains(5, compmoves)) {
                if (!contains(8, humanmoves)) {
                    return computerCanWinHelper(8);
                }

            }
            else if (contains(8, compmoves)) {
                if (!contains(5, humanmoves)) {
                    return computerCanWinHelper(5);
                }
                
            }
        }
        if (contains(3, compmoves)) {
            if (contains(9, compmoves)) {
                if (!contains(6, humanmoves)) {
                    return computerCanWinHelper(6);
                }
                
            }
            else if (contains(6, compmoves)) {
                if (!contains(9, humanmoves)) {
                    return computerCanWinHelper(9);
                }
                
            }
            else if (contains(5, compmoves)) {
                if (!contains(7, humanmoves)) {
                    return computerCanWinHelper(7);
                }
                 
            }
            else if (contains(7, compmoves)) {
                if (!contains(5, humanmoves)) {
                    return computerCanWinHelper(5);
                }
                
            }
        }
        if (contains(4, compmoves)) {
            if (contains(5, compmoves)) {
                if (!contains(6, humanmoves)) {
                    return computerCanWinHelper(6);
                }
                
            }
            else if (contains(6, compmoves)) {
                if (!contains(5, humanmoves)) {
                    return computerCanWinHelper(5);
                }
                
            }
            else if (contains(7, compmoves)) {
                if (!contains(1, humanmoves)) {
                    return computerCanWinHelper(1);
                }
                   
            }
        }
        if (contains(5, compmoves)) {
            if (contains(6, compmoves)) {
                if (!contains(4, humanmoves)) {
                    return computerCanWinHelper(4);
                }
                
            }
            else if (contains(8, compmoves)) {
                if (!contains(2, humanmoves)) {
                    return computerCanWinHelper(2);
                }
                
            }
            else if (contains(7, compmoves)) {
                if (!contains(3, humanmoves)) {
                    return computerCanWinHelper(3);
                }
                
            }
            else if (contains(9, compmoves)) {
                if (!contains(1, humanmoves)) {
                    return computerCanWinHelper(1);
                }
                
            }
        }
        if (contains(6, compmoves)) {
            if (contains(9, compmoves)) {
                if (!contains(3, humanmoves)) {
                    return computerCanWinHelper(3);
                }
                 
            }
        }
        if (contains(7, compmoves)) {
            if (contains(8, compmoves)) {
                if (!contains(9, humanmoves)) {
                    return computerCanWinHelper(9);
                }
                
            }
            else if (contains(9, compmoves)) {
                if (!contains(8, humanmoves)) {
                    return computerCanWinHelper(8);
                }
                  
            }
        }
        if (contains(8, compmoves)) {
            if (contains(9, compmoves)) {
                if (!contains(7, humanmoves)) {
                    return computerCanWinHelper(7);
                }
                
            }
        }

        return 0;
    }

    function computerCanWinHelper(i) {
        if (contains(i, humanmoves)) {
            return 0;
        }
        else {
            return i;
        }
    }

    function humanCanWin() {
        var winner = 0;
        if (contains(1, humanmoves)) {
            if (contains(2, humanmoves)) {
                if (!contains(3, compmoves)) {
                    winner = humanCanWinHelper(3);
                }
                
            }
            if (contains(3, humanmoves)) {
                if (!contains(2, compmoves)) {
                    winner = humanCanWinHelper(2);
                }
                
            }
            if (contains(4, humanmoves)) {
                if (!contains(7, compmoves)) {
                    winner = humanCanWinHelper(7);
                }
                
            }
            if (contains(5, humanmoves)) {
                if (!contains(9, compmoves)) {
                    winner = humanCanWinHelper(9);
                }
                
            }
            if (contains(7, humanmoves)) {
                if (!contains(4, compmoves)) {
                    winner = humanCanWinHelper(4);
                }
                
            }
            if (contains(9, humanmoves)) {
                if (!contains(5, compmoves)) {
                    winner = humanCanWinHelper(5);
                }
                
            }
        }
        if (contains(2, humanmoves)) {
            if (contains(3, humanmoves)) {
                if (!contains(1, compmoves)) {
                    winner = humanCanWinHelper(1);
                }
                
            }
            if (contains(5, humanmoves)) {
                if (!contains(8, compmoves)) {
                    winner = humanCanWinHelper(8);
                }

            }
            if (contains(8, humanmoves)) {
                if (!contains(5, compmoves)) {
                    winner = humanCanWinHelper(5);
                }
                
            }
        }
        if (contains(3, humanmoves)) {
            if (contains(9, humanmoves)) {
                if (!contains(6, compmoves)) {
                    winner = humanCanWinHelper(6);
                }
                
            }
            if (contains(6, humanmoves)) {
                if (!contains(9, compmoves)) {
                    winner = humanCanWinHelper(9);
                }
                
            }
            if (contains(5, humanmoves)) {
                if (!contains(7, compmoves)) {
                    winner = humanCanWinHelper(7);
                }
                 
            }
            if (contains(7, humanmoves)) {
                if (!contains(5, compmoves)) {
                    winner = humanCanWinHelper(5);
                }
                
            }
        }
        if (contains(4, humanmoves)) {
            if (contains(5, humanmoves)) {
                if (!contains(6, compmoves)) {
                    winner = humanCanWinHelper(6);
                }
                
            }
            if (contains(6, humanmoves)) {
                if (!contains(5, compmoves)) {
                    winner = humanCanWinHelper(5);
                }
                
            }
            if (contains(7, humanmoves)) {
                if (!contains(1, compmoves)) {
                    winner = humanCanWinHelper(1);
                }
                   
            }
        }
        if (contains(5, humanmoves)) {
            if (contains(6, humanmoves)) {
                if (!contains(4, compmoves)) {
                    winner = humanCanWinHelper(4);
                }
                
            }
            if (contains(8, humanmoves)) {
                if (!contains(2, compmoves)) {
                    winner = humanCanWinHelper(2);
                }
                
            }
            if (contains(7, humanmoves)) {
                if (!contains(3, compmoves)) {
                    winner = humanCanWinHelper(3);
                }
                
            }
            if (contains(9, humanmoves)) {
                if (!contains(1, compmoves)) {
                    winner = humanCanWinHelper(1);
                }
                
            }
        }
        if (contains(6, humanmoves)) {
            if (contains(9, humanmoves)) {
                if (!contains(3, compmoves)) {
                    winner = humanCanWinHelper(3);
                }
                 
            }
        }
        if (contains(7, humanmoves)) {
            if (contains(8, humanmoves)) {
                if (!contains(9, compmoves)) {
                    winner = humanCanWinHelper(9);
                }
                
            }
            if (contains(9, humanmoves)) {
                if (!contains(8, compmoves)) {
                    winner = humanCanWinHelper(8);
                }
                  
            }
        }
        if (contains(8, humanmoves)) {
            if (contains(9, humanmoves)) {
                if (!contains(7, compmoves)) {
                    winner = humanCanWinHelper(7);
                }
                
            }
        }

        return winner;
    }

    function humanCanWinHelper(i) {
        if (contains(i, compmoves)) {
            return 0;
        }
        else {
            return i;
        }
    }

    function contains(a, obj) {
        //console.log("contains, and array");
        //console.log(obj);
        //console.log(a);
        for (var i = 0; i < obj.length; i++) {
            if (obj[i] == a) {
                return true;
            }
        }
        return false;
    }
});