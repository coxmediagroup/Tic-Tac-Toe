define(function () {
    function Game() {
        this.board = $('gameboard');
        this.playerToken = null;
        this.aiToken = null;
        this.turn = null;

        this.tokens = {
            player: null, 
            ai: null
        };

        this.cells = this.board.querySelectorAll('.cell');
        this.listeners = {};
    }

    Game.prototype.addListeners = function() {
        var self = this;
        var updateCell = function() {
            if (self.turn === 'player') {
                self.markCell(this.id);
                self.removeListener(this.id);
                self.turn = 'ai';
            }
        };
        for (var i = 0; i < this.cells.length; i++) {
            this.cells[i].addEventListener('click', updateCell, false);
            this.listeners[this.cells[i].id] = updateCell;
        }
    };

    Game.prototype.removeListener = function(cell) {
        for (var i = 0; i < this.cells.length; i++) {
            if (this.cells[i].id === cell) {
                this.cells[i].removeEventListener('click', this.listeners[this.cells[i].id], false);
            }
        }
    };

    Game.prototype.markCell = function(cell) {
        for (var i = 0; i < this.cells.length; i++) {
            if (this.cells[i].id === cell) {
                this.cells[i].innerHTML = this.tokens[this.turn];
                this.cells[i].className = 'cell';
            }
        }
    };

    Game.prototype.update = function(response) {
        var data = JSON.parse(response);
        this.markCell(data.mark_cell);
        this.removeListener(data.mark_cell);
        if (this.turn === 'player') {
            this.turn = 'ai';
        } else {
            this.turn = 'player';
        }
    };

    Game.prototype.playerFirst = function() {
        this.turn = 'player';
        this.tokens.player = 'X';
        this.tokens.ai = 'O';
        this.addListeners();
        var request = new XMLHttpRequest();
        var self = this;
        request.onload = function() {
            self.update(this.response);
        };
        request.open('get', '/player_first/', true);
        request.send();
    };

    Game.prototype.aiFirst = function() {
        this.turn = 'ai';
        this.tokens.player = 'O';
        this.tokens.ai = 'X';
        this.addListeners();
        var request = new XMLHttpRequest();
        var self = this;
        request.onload = function() {
            self.update(this.response);
        };
        request.open('get', '/ai_first/', true);
        request.send();
    };

    return {
        Game: Game,
        board: null
    };
});
