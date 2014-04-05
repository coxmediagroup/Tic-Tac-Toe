var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
/// <reference path="Player.ts" />
/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    var ComputerPlayer = (function (_super) {
        __extends(ComputerPlayer, _super);
        function ComputerPlayer() {
            _super.call(this, "Computer Player");
        }
        ComputerPlayer.prototype.makeMove = function (boardIndex) {
            if (typeof boardIndex == "number") {
                _super.prototype.makeMove.call(this, boardIndex);
            } else {
                console.log(this.getLabel() + ' is using their wits...');
                var calculatedMove = 999;
                _super.prototype.makeMove.call(this, calculatedMove);
                return calculatedMove;
            }
        };

        ComputerPlayer.prototype.update = function (arg) {
            console.log('Computer player has been notified and ' + arg.player + ' made move at position #' + arg.madeMove);
        };
        return ComputerPlayer;
    })(TicTacToe.Player);
    TicTacToe.ComputerPlayer = ComputerPlayer;
})(TicTacToe || (TicTacToe = {}));
