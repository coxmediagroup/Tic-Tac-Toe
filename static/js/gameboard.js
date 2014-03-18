define(function () {
    function GameBoard(host, port) {
        this.board = $('gameboard');
        this.host = host;
        this.port = port;
        this.uri = 'http://' + this.host + ':' + this.port;
        this.playerToken = null;
        this.aiToken = null;

        this.cells = this.board.querySelectorAll('.cell');
    }

    GameBoard.prototype.addListeners = function() {
        var self = this;
        var updateCell = function() {
            this.innerHTML = self.playerToken;
        };
        for (var i = 0; i < this.cells.length; i++) {
            this.cells[i].addEventListener('click', updateCell);
        }
    };

    GameBoard.prototype.playerFirst = function() {
        this.playerToken = 'X';
        this.aiToken = 'O';
        this.addListeners();
        var request = new XMLHttpRequest();
        request.onload = this.update;
        request.open('get', this.uri + '/player_first/', true);
        request.send();
    };

    GameBoard.prototype.aiFirst = function() {
        this.playerToken = 'O';
        this.aiToken = 'X';
        this.addListeners();
        var request = new XMLHttpRequest();
        request.onload = this.update;
        request.open('get', this.uri + '/ai_first/', true);
        request.send();
    };

    GameBoard.prototype.update = function(response) {
    };

    return GameBoard;
});
