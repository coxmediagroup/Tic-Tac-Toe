define(['cell'], function (Cell) {
    function Game() {
        this.board = $('gameboard');
        this.narrative = $('narrative');
        this.turn = null;

        this.tokens = {
            player: null,
            ai: null
        };

        this.cells = {};
        var cells = this.board.querySelectorAll('.cell');
        for (var i = 0; i < cells.length; i++) {
            var cell = new Cell(cells[i]);
            this.cells[cells[i].id] = cell;
        }
    }

    Game.prototype.update = function() {
        if (this.status !== 200) {
            // sad pants
            return;
        }
        var data = JSON.parse(this.response);
        this.board.cells[data.mark_cell].mark(this.board.tokens[this.board.turn]);
        if (this.board.turn === 'player') {
            this.board.turn = 'ai';
        } else {
            this.board.turn = 'player';
            this.board.narrative.innerHTML = '';
        }
    };

    Game.prototype.playerFirst = function() {
        this.turn = 'player';
        this.tokens.player = 'X';
        this.tokens.ai = 'O';

        var request = new XMLHttpRequest();
        var self = this;
        request.onload = function() {};
        request.open('get', '/player_first/', true);
        request.send();
    };

    Game.prototype.aiFirst = function() {
        this.turn = 'ai';
        this.tokens.player = 'O';
        this.tokens.ai = 'X';

        for (var key in this.cells) {
            this.cells[key].enable(this.tokens.player);
        }

        var request = new XMLHttpRequest();
        request.board = this;
        var self = this;
        request.onload = this.update;
        request.open('get', '/ai_first/', true);
        request.send();
    };

    return {
        Game: Game,
        board: null
    };
});
