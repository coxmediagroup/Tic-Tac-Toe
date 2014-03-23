define(['cell'], function (Cell) {
    function Game() {
        this.board = $('gameboard');
        this.initialStart = $('initial-start');
        this.restart = $('restart');
        this.messages = $('messages');

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

    Game.prototype.aiResponse = function(responseData) {
        this.hideMessage();

        if (responseData.mark_cell !== undefined) {
            this.cells[responseData.mark_cell].mark(this.tokens.ai);
        }

        if (responseData.draw_cell !== undefined) {
            // player trying to force a draw
            this.cells[responseData.draw_cell].angry();
            this.showMessage(responseData.message);
            return;
        }

        if (responseData.winning_cells === undefined) {
            return;
        }
        // winner winner chicken dinner
        // disable all cells since there is a winner
        for (var key in this.cells) {
            this.cells[key].disable();
        }

        for (var i = 0; i < responseData.winning_cells.length; i++) {
            var cellName = responseData.winning_cells[i];
            this.cells[cellName].winner();
        }

        // prompt for restart
        this.restart.style.display = 'block';
    };

    Game.prototype.aiFirst = function() {
        this.hideRestart();
        this.hideMessage();
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

    Game.prototype.showMessage = function(message) {
        this.messages.innerHTML = message;
        this.messages.style.display = '';
    };

    Game.prototype.hideMessage = function() {
        this.messages.style.display = 'none';
    };

    Game.prototype.hideRestart = function() {
        this.restart.style.display = 'none';
    };

    Game.prototype.showRestart = function() {
        this.restart.style.display = '';
    };

    return {
        Game: Game,
        board: null
    };
});
