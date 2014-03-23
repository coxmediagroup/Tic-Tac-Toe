define(function() {
    function Cell(element, board) {
        this.element = element;
        this.board = board;
        this.id = this.element.id;
        this.playerToken = null;
    }

    Cell.prototype.enable = function(playerToken) {
        this.playerToken = playerToken;
        var self = this;
        this.onClick = function() {
            var request = new XMLHttpRequest();
            request.onload = function() {
                if (this.status === 200) {
                    self.mark(self.playerToken);
                    self.board.aiResponse(this.response);
                    return;
                }
                // swallow errors
            };
            var url = '/player_turn/' + self.id + '/';
            request.open('get', url, true);
            request.send();
        };
        this.element.addEventListener('click', this.onClick, false);
    };

    Cell.prototype.disable = function() {
        this.element.className = 'cell'; // removes the 'active' class (to disable hover effect)
        this.element.removeEventListener('click', this.onClick, false);
    };

    Cell.prototype.mark = function(token) {
        this.element.innerHTML = token;
        this.disable();
    };

    Cell.prototype.winner = function() {
        this.element.className = 'cell winner';
    };

    return Cell;
});
