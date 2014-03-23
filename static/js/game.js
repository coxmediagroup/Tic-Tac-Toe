define(['cell'], function (Cell) {
    function Game() {
        this.board = $('gameboard');
        this.initialStart = $('initial-start');
        this.restart = $('restart');

        this.tokens = {
            player: null,
            ai: null
        };

        this.cells = {};
        var cells = this.board.querySelectorAll('.cell');
        for (var i = 0; i < cells.length; i++) {
            var cell = new Cell(cells[i], this);
            this.cells[cells[i].id] = cell;
        }
    }

    Game.prototype.aiResponse = function(response) {
        var data = JSON.parse(response);
        this.cells[data.mark_cell].mark(this.tokens.ai);
        if (data.winning_cells === undefined) {
            return;
        }

        // disable all cells since there is a winner
        for (var key in this.cells) {
            this.cells[key].disable();
        }

        for (var i = 0; i < data.winning_cells.length; i++) {
            var cellName = data.winning_cells[i];
            this.cells[cellName].winner();
        }

        // prompt for restart
        this.restart.style.display = 'block';
    };

    Game.prototype.aiFirst = function() {
        this.restart.style.display = 'none';
        this.tokens.player = 'O';
        this.tokens.ai = 'X';

        for (var key in this.cells) {
            this.cells[key].enable(this.tokens.player);
        }

        var request = new XMLHttpRequest();
        request.board = this;
        var self = this;
        request.onload = function() {
            if (this.status != 200) {
                // sad pants
                return;
            }
            var data = JSON.parse(this.response);
            self.cells[data.mark_cell].mark(self.tokens.ai);
            self.initialStart.style.display = 'none';
        };
        request.open('get', '/ai_first/', true);
        request.send();
    };

    return {
        Game: Game,
        board: null
    };
});
