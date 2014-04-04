/// <reference path="TicTacToe.ts" />
var TicTacToe;
(function (TicTacToe) {
    var HumanPlayer = (function () {
        function HumanPlayer() {
            this.label = 'Human Player';
        }
        return HumanPlayer;
    })();
    TicTacToe.HumanPlayer = HumanPlayer;
})(TicTacToe || (TicTacToe = {}));
