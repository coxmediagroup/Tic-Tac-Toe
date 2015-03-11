(function() {
    'use strict';

    // global state variables
    var gameOver = false,
        usersTurn = true,
        board = '---------';

    function displayBoard() {
        var char;
        for (var i=0; i<9; i++) {
            char = board.charAt(i);
            // don't display - chars, use '' instead
            if (char === '-') char = '';
            $("#cell-" + i).text(char);
        }
        changeStateOfRestartButton('enabled');
    }

    function handleAiMove() {
        // don't process user's move until AI has moved.
        usersTurn = false;

        // have AI evaluate board, then display results
        var f = function() {
            $.getJSON("/evalBoard?board="+board)
                .done(function(data) {
                    // AI returns 3 values: new board, status, and winning positions
                    board = data.board;
                    var status = data.status;
                    var positions = data.positions;

                    displayBoard();

                    switch(status) {
                        case 'continue':
                            setStatus("Your turn.");
                            break;

                        case 'iwin':
                            setStatus("I won!");
                            highlightPositions(positions);
                            gameOver = true;
                            break;

                        case 'uwin':
                            setStatus("You won!");
                            highlightPositions(positions);
                            gameOver = true;
                            break;

                        case 'draw':
                            setStatus("We tied.");
                            gameOver = true;
                            break;

                        default:
                            alert("bad status = "+status);
                    }
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Error!\ntextStatus = " + textStatus + "\nerrorThrown = " + errorThrown);
                })
                .always(function() {
                    // AI done, so it's ok for user to move.
                    usersTurn = true;
                });
        };

        // wait half a sec so that AI's response feels more human
        setTimeout(f, 500);
    }

    function highlightPositions(positions) {
        var position;
        for (var i=0; i<positions.length; i++) {
            position = positions[i];
            $("#cell-" + position).addClass('highlighted');
        }
    }

    function changeStateOfRestartButton(state) {
        if (state === 'disabled') {
            $("#restart").prop('disabled', true).addClass('disabled');
        } else {
            $("#restart").prop('disabled', false).removeClass('disabled');
        }
    }

    function setStatus(msg) {
        $("#status").html(msg);
    }

    //////////////////////////////////////////////////////////////////////////
    // Event handlers
    //////////////////////////////////////////////////////////////////////////
    function handleUserMove(event) {
        var $clickedCell, index, boardList;

        if (usersTurn !== true) {
            setStatus("Sorry, it's not your turn yet");
            return;
        }

        if (gameOver === true) {
            setStatus("Sorry, game over!");
            return;
        }

        $clickedCell = $(event.target);
        if ($clickedCell.text() !== '') {
            setStatus("Sorry, you can't move there...");
            return;
        }

        setStatus("");

        index = $clickedCell.attr('id').split('-')[1];

        // change board at position = index to 'X'
        boardList = board.split('');
        boardList[index] = 'X';
        board = boardList.join('');

        // reflect user's move
        displayBoard();

        handleAiMove();
        return;
    }

    function startOver() {
        // set global state vars
        gameOver = false;
        usersTurn = true;
        board = '---------';

        $("td").removeClass('highlighted');

        displayBoard();
        setStatus("Make your first move or click <a href data-action='ai-starts'>here</a> and I'll start.");
        changeStateOfRestartButton('disabled');
    }

    function statusClicked(event) {
        event.preventDefault();
        var $target = $(event.target);
        if ($target.attr('data-action') === 'ai-starts') {
            handleAiMove();
        }
    }

    //////////////////////////////////////////////////////////////////////////

    (function() {
        // hookup our event handlers
        $("td").click(handleUserMove);
        $("#restart").click(startOver);
        $("#status").click(statusClicked);

        startOver();
    })();

})();
