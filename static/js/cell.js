define(function() {
    function Cell(element, board) {
        this.element = element;
        this.board = board;
        this.id = this.element.id;
        this.playerToken = null;
    }

    Cell.prototype.enable = function(playerToken) {
        this.playerToken = playerToken;
        this.element.className = 'cell active';
        this.element.innerHTML = '';
        var self = this;
        this.onClick = function() {
            var request = new XMLHttpRequest();
            request.onload = function() {
                if (this.status === 200) {
                    var data = JSON.parse(this.response);
                    if (data.mark_cell !== undefined) {
                        // if 'mark_cell' isn't present the player is trying to force a draw, so don't mark
                        self.mark(self.playerToken);
                    }
                    self.board.aiResponse(data);
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

    Cell.prototype.angry = function() {
        this.disable();
        this.element.innerHTML = '(>_<)';
        this.element.className = 'cell angry';
    };

    return Cell;
});
