angular.module('tttApp').controller('tttBasicGameCtrl', function ($scope) {

    var game = new Game(3, 3);
    $scope.game = game;
    $scope.currentPlayer = 1;
    
    $scope.move = function (col, row) {
        game.makeMove(col, row, $scope.currentPlayer);
        $scope.currentPlayer = SetNextPlayer($scope.currentPlayer);
    };

    function SetNextPlayer(currentPlayer) {
        if (currentPlayer === 1) return 2;
        else return 1;
    }

});


function Game(cols, rows) {
    this.columnsCount = cols;
    this.rowCount = rows;
    this.pos1 = 0;
    this.gameBoard = [[0,0,2],[0,0,0],[0,0,0]];
    this.makeMove = function (col, row, player) {
        this.gameBoard[col][row] = player;

    };

}