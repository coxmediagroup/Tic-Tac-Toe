/// <reference path="TicTacToe.ts" />
var TicTacToe;
(function (TicTacToe) {
    var ComputerPlayer = (function () {
        function ComputerPlayer() {
            this.label = 'Computer Player';
        }
        return ComputerPlayer;
    })();
    TicTacToe.ComputerPlayer = ComputerPlayer;
})(TicTacToe || (TicTacToe = {}));
