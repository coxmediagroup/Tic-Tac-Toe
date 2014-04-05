var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
/// <reference path="Observable.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Player = (function (_super) {
        __extends(Player, _super);
        function Player(_label) {
            _super.call(this);
            this._label = _label;
            this._score = 0;
            this._playedMoves = [];
        }
        Player.prototype.makeMove = function (boardIndex) {
            this._playedMoves.push(boardIndex);
            this.notifyObservers({ player: this._label, madeMove: boardIndex });
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
    })(TicTacToe.Observable);
    TicTacToe.Player = Player;
})(TicTacToe || (TicTacToe = {}));
