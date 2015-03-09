(function() {
    'use strict';

    //////////////////////////////////////////////////////////////
    // App-Specific Functions
    //////////////////////////////////////////////////////////////
    // global state variables
    var gameOver = false,
        board = '---------';

    function setStatus(msg) {
        $("#status").html(msg);
    }

    function startOver() {
        // set global state vars
        gameOver = false;
        board = '---------';

        displayBoard();
        setStatus("You're X and I'm O...  You go first!");
    }

    function displayBoard() {
        var char;
        for (var i=0; i<9; i++) {
            char = board.charAt(i);
            if (char === '-') char = '';
            $("#cell-" + i).text(char);
        }
    }

    function handleUserMove(event) {
        var $clickedCell, index, boardList, jqxhr;

        if (gameOver === true) {
            setStatus("Sorry, game over!");
            return;
        }

        $clickedCell = $(event.target);
        if ($clickedCell.text() !== '') {
            setStatus("Sorry, you can't move there...");
            return;
        }

        setStatus("Ok, my turn...");

        index = $clickedCell.attr('id').split('-')[1];

        // change board at position index to 'X'
        boardList = board.split('');
        boardList[index] = 'X';
        board = boardList.join('');

        // reflect user's move
        displayBoard();

        // have AI evaluate board, then display results
        var f = function() {
            jqxhr = $.getJSON("/evalBoard?board="+board);
            jqxhr.done(function(data) {
                board = data.board;
                displayBoard();

                status = data.status;
                switch(status) {
                    case 'continue':
                        setStatus("Your move again...");
                        break;

                    case 'iwin':
                        setStatus("I won!");
                        gameOver = true;
                        break;

                    case 'uwin':
                        setStatus("You won!");
                        gameOver = true;
                        break;

                    case 'draw':
                        setStatus("We tied.");
                        gameOver = true;
                        break;

                    default:
                        alert("bad status = "+status);
                }
                console.log("success! data =", data, JSON.stringify(data));
            });
            jqxhr.fail(function(jqXHR, textStatus, errorThrown) {
                alert("Error!\ntextStatus = " + textStatus + "\nerrorThrown = " + errorThrown);
            });
        };

        setTimeout(f, 500);

        return;
    }

    //////////////////////////////////////////////////////////////////////////

    function init() {
        $("td").click(handleUserMove);
        startOver();

    }

    init();
})();
