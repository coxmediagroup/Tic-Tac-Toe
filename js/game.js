/*
 Set the board to be ready for play.
 */
function setBoard() {

    //Determine if the game options are set to begin play
    var optionsAreEmpty = false;
    $('.control > option:selected').each(function (index, value) {
        if ($(value).val() === '') {
            optionsAreEmpty = true;
        } else {
            if ($(value).parent().prop('id') == 'human-piece') {
                window.humanPiece = $(value).val();
            }
            if ($(value).parent().prop('id') == 'first-player') {
                window.firstPlayer = $(value).val();
                window.whoseTurn = $(value).val();
            }
            //Set the machine game piece based on the human piece
            if (humanPiece == 'O') {
                machinePiece = 'X';
            } else {
                machinePiece = 'O';
            }
        }
        ;
    });

    if (optionsAreEmpty) {
        alert('Select game options first.');
        return;
    }
    ;


    //Set the visual cues that the board is ready
    $('#game-board td').css('cursor', 'pointer');
    $('#game-board td').css('background-color', '#fff');
    $('#game-board td').css('border-color', '#e7e7e7');

    //Disable options to prevent confusion if they are changed mid game
    $('.control').attr('disabled', true);
    $('#set-board').text('Game in Progress').attr('disabled', true);


    $('#game-board td').bind('click', function (event) {
        humanMove(event);
    });


    if (whoseTurn == 'Human') {
        humanMove()
    } else {
        machineMove()
    }
}

/*
 Close the board for play
 */
function closeBoard() {
    //Set visual cues that the gameboard is not available
    $('#game-board td').css('cursor', 'not-allowed');
    $('#game-board td').css('background-color', '#e7e7e7');
    $('#game-board td').css('border-color', '#999');

    //Allow new options to be set for a new game
    $('.control').attr('disabled', false);
    $('#set-board').text('Play Again').attr('disabled', false);
}


/*
 Speed up development with debug features
 */
function devDebug(piece, player) {
    piece = piece || 'X';
    player = player || 'Human';
    $('#human-piece').val(piece);
    $('#first-player').val(player);
    setBoard();
}

/*
 Show numbers in matrix box to help visualize winning moves
 */
function devShowMatrix() {
    $.each($('#game-board td'), function (index, value) {
        $(value).text($(value).prop('id'))
    });
}

function humanMove(event) {
    //prevent someone from clicking faster than a slow machine
    if (window.whoseTurn == 'Machine') {
        return;
    }

    gameMessage();

    //This square hasn't been played by someone yet
    if (event && $(event.target).prop('id') != 'set-board' && !$(event.target).data('playedBy')) {
        $(event.target).text(window.humanPiece).addClass('played').data('playedBy', 'Human');
        var existingMoves = '';
        if (typeof  $('#game-board').data('humanMoves') != 'undefined') {
            existingMoves = $('#game-board').data('humanMoves');
        }

        $('#game-board').data('humanMoves', existingMoves + $(event.target).prop('id') + '|');  //store human moves as a string

        window.whoseTurn = 'Machine';
    }

    machineMove();
}

function machineMove() {
    var testedCombos = new Array();
    gameMessage();
    var almostWin = checkAlmostWin();
    if(almostWin){
        $(almostWin).text(window.machinePiece).addClass('played').data('playedBy', 'Machine');
        if(checkWinner() === true){
            alert ('I won');
            return;
        }

    }
    //Collect the moves made by a human so far
    var humanMoves;
    if($('#game-board').data('humanMoves')){
        humanMoves = $('#game-board').data('humanMoves').split('|');

        if (humanMoves[humanMoves.length - 1] === '') {
            humanMoves.splice(humanMoves.length - 1, 1)
        }
    }

    var risk = 0;
    var stopAWinCombo;
    var stopFirstAttemptCombo;
    var i, n;
    //Loop through the human moves to test for winning moves
    if(humanMoves) {
        for (i = 0; i < humanMoves.length; i++) {

            //Loop through the winning move combos
            for (var combo = 0; combo < winningMoves.length; combo++) {

                //Does this particular combination have this particular human move? Has it been tested before?
                if (winningMoves[combo].search(humanMoves[i]) > -1 && testedCombos.indexOf(winningMoves[combo]) == -1) {
                    risk = 1;
                    testedCombos.push(winningMoves[combo]); // Keep track of tested Combos so we don't repeat effort
                    var possibleWinner = winningMoves[combo];

                    for (n = 0; n < possibleWinner.length; n++) {
                        var cell = '#' + possibleWinner.charAt(n);
                        if ($(cell).hasClass('played') && $(cell).data('playedBy')=='Human') {
                            risk = risk + 1;
                        }
                        if (risk == 2) {
                            stopFirstAttemptCombo = possibleWinner;
                        }

                        if (risk == 3) {
                            stopAWinCombo = possibleWinner;
                        }
                    }

                }

            }

            if (stopAWinCombo) {
                for (n = 0; n < stopAWinCombo.length; n++) {
                    var cell = '#' + stopAWinCombo.charAt(n);
                    if (!$(cell).hasClass('played') ) {
                        $(cell).text(window.machinePiece).addClass('played').data('playedBy', 'Machine');
                        window.whoseTurn = 'Human';
                        break;
                        }
                    }

            }

            if (stopFirstAttemptCombo && window.whoseTurn == 'Machine') {
                //look for an empty cell to fill
                for (n = 0; n < stopFirstAttemptCombo.length; n++) {

                    var cell = '#' + stopFirstAttemptCombo.charAt(n);
                    if (!$(cell).hasClass('played') ) {
                        $(cell).text(window.machinePiece).addClass('played').data('playedBy', 'Machine');
                        window.whoseTurn = 'Human'
                        break;
                    }
                }
;
            }

            //No strategic move left, just make a generic move
            if(window.whoseTurn == 'Machine'){
                //look for an empty cell to fill
                for (n = 0; n < 9; n++) {

                    var cell = '#' + n;
                    if (!$(cell).hasClass('played') ) {
                        $(cell).text(window.machinePiece).addClass('played').data('playedBy', 'Machine');
                        break;
                    }
                }
                window.whoseTurn = 'Human';
            }

        }
    }
    if(checkWinner() === true){
        alert ('I won');
    }
    gameMessage();
}

function gameMessage() {
    if (window.whoseTurn == 'Machine') {
        $('#message-cell').text('Machine is thinking');
    } else {
        $('#message-cell').text('Human - it is your turn');
    }

}

/*
    See if there is a winner yet
 */
function checkWinner(){
    var winner = false;
    var i,n;
    //iterate through winning combos
    for (i = 0; i < winningMoves.length; i++) {
        var winning = 0;
        for(var n = 0; n < winningMoves[i]; n++) {
            var cell = '#' + winningMoves[i].charAt(n);
            if ($(cell).hasClass('played') && $(cell).data('playedBy') == 'Machine') {
                winning = winning + 1;
            }
            if (winning == 3) {
                $('#message-cell').text('I won');
                //$('.control').attr('disabled', false);  //  FIXME: Game doesn't support replay yet
                //$('#set-board').text('Game Over').attr('disabled', false);

                winner = true;
                break;

            }
        }

    }



    return winner;
}

/*
    Check for an almost win to prevent losing y playing defense
 */
function checkAlmostWin(){
    var i,n;
    for (i = 0; i < winningMoves.length; i++) {
        var winning = 0;
        var available = -1;
        for(n = 0; n < winningMoves[i]; n++) {
            var cell = '#' + winningMoves[i].charAt(n);
            if ($(cell).hasClass('played') && $(cell).data('playedBy') == 'Human') {
                continue;
            } // A human already blocked this move
            if ($(cell).hasClass('played') && $(cell).data('playedBy') == 'Machine') {
                winning = winning + 1;
            }
            if (!$(cell).hasClass('played')) {
                available = cell;
            }

            if (winning == 2 && available != -1) {
                return available
                break;
            }
        }
    }
    return false
}