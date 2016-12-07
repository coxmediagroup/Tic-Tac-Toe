var TicTacToe;
(function (TicTacToe) {
    var Player = (function () {
        function Player(_label) {
            this._label = _label;
            this._score = 0;
            this._playedMoves = [];
        }
        Player.prototype.makeMove = function (boardIndex) {
            this._playedMoves.push(boardIndex);
            console.log(this._label + ' played position #' + boardIndex);
        };

        // TODO: Set the compiler to output ECMAScript 5 and convert to a proper getter.
        Player.prototype.getLabel = function () {
            return this._label;
        };

        Player.prototype.getScore = function () {
            return this._score;
        };

        Player.prototype.setScore = function (score) {
            this._score = score;
        };
        return Player;
    })();
})(TicTacToe || (TicTacToe = {}));
