var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
/// <reference path="TicTacToe.ts" />
var TicTacToe;
(function (TicTacToe) {
    var HumanPlayer = (function (_super) {
        __extends(HumanPlayer, _super);
        function HumanPlayer() {
            _super.call(this, "Human Player");
        }
        return HumanPlayer;
    })(TicTacToe.Player);
    TicTacToe.HumanPlayer = HumanPlayer;
})(TicTacToe || (TicTacToe = {}));
