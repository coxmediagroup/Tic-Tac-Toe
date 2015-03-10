(function() {
    'use strict';

    // global state variables
    var gameOver = false,
        board = '---------';

    function displayBoard() {
        var char;
        for (var i=0; i<9; i++) {
            char = board.charAt(i);
            if (char === '-') char = '';
            $("#cell-" + i).text(char);
        }
        restartButton('enabled');
    }

    function handleAiMove() {
        // have AI evaluate board, then display results
        var jqxhr;
        var f = function() {
            jqxhr = $.getJSON("/evalBoard?board="+board);
            jqxhr.done(function(data) {
                // console.log(data);
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
            });
            jqxhr.fail(function(jqXHR, textStatus, errorThrown) {
                alert("Error!\ntextStatus = " + textStatus + "\nerrorThrown = " + errorThrown);
            });
        };

        // f();

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

    function restartButton(state) {
        if (state === 'disabled') {
            $("#restart").prop('disabled', true).addClass('disabled');
        } else {
            $("#restart").prop('disabled', false).removeClass('disabled');
        }
    }

    function handleUserMove(event) {
        var $clickedCell, index, boardList;

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

        // change board at position index to 'X'
        boardList = board.split('');
        boardList[index] = 'X';
        board = boardList.join('');

        // reflect user's move
        displayBoard();

        handleAiMove();
        return;
    }

    function setStatus(msg) {
        $("#status").html(msg);
    }

    function startOver() {
        // set global state vars
        gameOver = false;
        board = '---------';

        $("td").removeClass('highlighted');

        displayBoard();
        setStatus("Make your first move or click <a href data-action='ai-starts'>here</a> and I'll start.");
        restartButton('disabled');
    }

    function statusClicked(event) {
        event.preventDefault();
        var $target = $(event.target);
        if ($target.attr('data-action') === 'ai-starts') {
            handleAiMove();
        }
    }

    //////////////////////////////////////////////////////////////////////////

    function init() {
        $("td").click(handleUserMove);
        $("#restart").click(startOver);
        $("#status").click(statusClicked);
        startOver();
    }

    init();
})();
