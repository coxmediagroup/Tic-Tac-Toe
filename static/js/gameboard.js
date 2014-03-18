define(function () {
    function GameBoard(playerToken) {
        this.board = $('gameboard');
        this.playerToken = playerToken;

        this.cells = this.board.querySelectorAll('.cell');
        for (var i = 0; i < this.cells.length; i++) {
            this.cells[i].addEventListener('click', function() {
                this.innerHTML = 'X';
            });
        }
    }

    return GameBoard;
});
