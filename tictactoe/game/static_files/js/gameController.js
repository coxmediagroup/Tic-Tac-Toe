var turn = -1;
var xWon = 0;
var oWon = 0;
var catsGame = 0;
var cells;
	
$(document).ready(function() {
	buildBoard();
});

function buildBoard(){
    var b = document.board;
    cells = new Array(b.c1,b.c2,b.c3,b.c4,b.c5,b.c6,b.c7,b.c8,b.c9)
}

function getValidMoves(state){
    var moves = 0;
    for (var i=0; i<9; i++){
        if ((state & (1<<(i*2+1))) == 0){
            moves |= 1 << i;
        }
    }
    return moves;
}

function placeComputerTokenRandomly(moves){
    var numberOfMoves = 0;
    for (var i=0; i<9; i++){
        if ((moves & (1<<i)) != 0) numberOfMoves++;
    }
    if (numberOfMoves > 0){
        var movesNumber = Math.ceil(Math.random()*numberOfMoves);
        numberOfMoves = 0;
        for (var j=0; j<9; j++){
            if ((moves & (1<<j)) != 0) numberOfMoves++;
            if (numberOfMoves == movesNumber){
                markGrid(cells[j]);
                return;
            }
        }
    }
}

function checkBoard(state){
    var mask = state & 0x2AAAA;	
    if (mask == 0x00000) return 0x1FF;
	if (mask == 0x00200) return 0x145;
    if (mask == 0x00002 ||
        mask == 0x00020 ||
        mask == 0x02000 ||
        mask == 0x20000) return 0x010;
    if (mask == 0x00008) return 0x095;
    if (mask == 0x00080) return 0x071;
    if (mask == 0x00800) return 0x11C;
    if (mask == 0x08000) return 0x152;
    return 0;
}

function moveValue(istate, move, moveFor, nextTurn, limit, depth){
    var state = stateMove(istate, move, nextTurn);
    var winner = checkForWin(state);
    if ((winner & 0x300000) == 0x300000){
        return 0;
    } else if (winner != 0){
        if (moveFor == nextTurn) return 10 - depth;
        else return depth - 10;
    }
    var anticipate = 999;
    if (moveFor != nextTurn) anticipate = -999;
    if(depth == limit) return anticipate;
    var moves = getValidMoves(state);
    for (var i=0; i<9; i++){
        if ((moves & (1<<i)) != 0) {
            var value = moveValue(state, i, moveFor, -nextTurn, 10-Math.abs(anticipate), depth+1);
            if (Math.abs(value) != 999){
                if (moveFor == nextTurn && value < anticipate){
                    anticipate = value;
                } else if (moveFor != nextTurn && value > anticipate){
                    anticipate = value;
                }
            }
        }
    }
    return anticipate;
}

function getState(){
    var state = 0;
    for (var i=0; i<9; i++){
        var cell = cells[i];
        var value = 0;
        if (cell.value.indexOf('X') != -1) value = 0x3;
        if (cell.value.indexOf('O') != -1) value = 0x2;
        state |= value << (i*2);
    }
    return state;
}

function checkForWin(state){
    if ((state & 0x3F000) == 0x3F000) return 0x13F000;
    if ((state & 0x3F000) == 0x2A000) return 0x22A000;
    if ((state & 0x00FC0) == 0x00FC0) return 0x100FC0;
    if ((state & 0x00FC0) == 0x00A80) return 0x200A80;
    if ((state & 0x0003F) == 0x0003F) return 0x10003F;
    if ((state & 0x0003F) == 0x0002A) return 0x20002A;
    if ((state & 0x030C3) == 0x030C3) return 0x1030C3;
    if ((state & 0x030C3) == 0x02082) return 0x202082;
    if ((state & 0x0C30C) == 0x0C30C) return 0x10C30C;
    if ((state & 0x0C30C) == 0x08208) return 0x208208;
    if ((state & 0x30C30) == 0x30C30) return 0x130C30;
    if ((state & 0x30C30) == 0x20820) return 0x220820;
    if ((state & 0x03330) == 0x03330) return 0x103330;
    if ((state & 0x03330) == 0x02220) return 0x202220;
    if ((state & 0x30303) == 0x30303) return 0x130303;
    if ((state & 0x30303) == 0x20202) return 0x220202;
    if ((state & 0x2AAAA) == 0x2AAAA) return 0x300000;
    return 0;
}

function recordWin(winner){
    if ((winner & 0x300000) == 0x100000){
        xWon++;
    } else if ((winner & 0x300000) == 0x200000){
        oWon++;
    } else if ((winner & 0x300000) == 0x300000){
        catsGame++; 
    }
    displayStats();
}

function displayStats(){

    var b = document.board;
	var totalGames = xWon + oWon + catsGame;
    b.xWon.value = xWon;
    b.oWon.value = oWon;
    b.catsGame.value = catsGame;
}

function clearStats(){
	xWon = 0;
    oWon = 0;
    catsGame = 0;
    displayStats();
}

function checkoutState(state){
    var winner = checkForWin(state);
    if ((winner & 0x300000) != 0){
        if ((winner & 0x300000) == 0x100000){
            xWon++;
			document.getElementById("prompt").innerHTML="You won!";
        } else if ((winner & 0x300000) == 0x200000){
            oWon++;
			document.getElementById("prompt").innerHTML="You Lost!";
        } else {
			document.getElementById("prompt").innerHTML="It\'s a draw.";
            catsGame++;
        }
        displayStats();
    }
    for (var i=0; i<9; i++){
        var value = '';
        if ((state & (1<<(i*2+1))) != 0){
            if ((state & (1<<(i*2))) != 0){
                value = 'X';
            } else {
                value = 'O';
            }
        }
        if ((winner & (1<<(i*2+1))) != 0){
            if (cells[i].style){
                cells[i].style.backgroundColor='#00a9e0';
            } else {
                value = '*' + value + '*';
            }
        } else {
            if (cells[i].style){
                cells[i].style.backgroundColor='#D9D9D9';
            }
        }
        cells[i].value = value;
    }
}

function stateMove(state, move, nextTurn){
    var value = 0x3;
    if (nextTurn == -1) value = 0x2;
    return (state | (value << (move*2)));
}

function markGrid(cell){
    if (cell.value == ''){
        var state = getState();
        var winner = checkForWin(state);
        if (winner == 0){
            for (var i=0; i<9; i++){
                if (cells[i] == cell){
                    state = stateMove(state, i, turn);
                }
            }
            checkoutState(state);
            nextTurn();
        }
    }
}

function countMoves(state){
    var count = 0;
    for (var i=0; i<9; i++){
        if ((state & (1<<(i*2+1))) != 0){
           count++;
        }
    }
    return count;
}

function computerTurn(){
    var state = getState();
    var winner = checkForWin(state);
    if (winner == 0){
        var moves = getValidMoves(state);
        var anticipate = -999;
        var goodMoves = checkBoard(state);
        if (goodMoves == 0){
            for (var i=0; i<9; i++){
                if ((moves & (1<<i)) != 0) {
                    var value = moveValue(state, i, turn, turn, 15, 1);
                    if (value > anticipate){
                        anticipate = value;
                        goodMoves = 0;
                    }
                    if (anticipate == value){
                        goodMoves |= (1<<i);
                    }
                }
            }
        }
        placeComputerTokenRandomly(goodMoves);
    }
}

function nextTurn(){
    turn = -turn;
    if (turn == -1){ 
		computerTurn(); 
    }
}

function newGame(){
    var state = getState();
    var winner = checkForWin(state);
	document.getElementById("prompt").innerHTML="";
    if (winner == 0 && countMoves(state) > 1){
        if (turn == 1) oWon++;
        else xWon++;
        displayStats();
    }
    checkoutState(0);
    if (document.board.firstMove[0].checked=='1'){
        turn = -1;
    } else {
        turn = 1;
    }
    nextTurn();
}