define(['cell'], function (Cell) {
    function Game() {
        this.board = $('gameboard');
        this.narrative = $('narrative');

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
    };

    Game.prototype.playerFirst = function() {
        this.tokens.player = 'X';
        this.tokens.ai = 'O';

        var request = new XMLHttpRequest();
        var self = this;
        request.onload = function() {};
        request.open('get', '/player_first/', true);
        request.send();
    };

    Game.prototype.aiFirst = function() {
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
            self.narrative.innerHTML = '';
        };
        request.open('get', '/ai_first/', true);
        request.send();
    };

    return {
        Game: Game,
        board: null
    };
});
