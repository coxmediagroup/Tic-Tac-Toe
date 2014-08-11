angular.module('tttApp').controller('tttBasicGameCtrl', function ($scope, $http) {

    var game = new Game(3, 3);
    $scope.game = game;
    $scope.currentPlayer = 1;

    //need the controller to abstract out the UI needing to know whos turn it is
    $scope.move = function (col, row) {

        if ($scope.currentPlayer === 1) {
            var result = game.makeMove(col, row, $scope.currentPlayer);
            if (result) $scope.currentPlayer = SetNextPlayer($scope.currentPlayer);
            //ai turn
            var request = $http({
                method: 'PUT',
                url: '/api/game',
                data: game.gameBoard
            }).success(function (data, status, headers, config) {
                game.gameBoard = data.gameBoard;

                if (data.winner !== 0) {
                    if (data.winner === 1) {
                        alert('player 1 wins');
                    }
                    else if (data.winner === 2) {
                        alert('computer wins!');
                    }
                    else {
                        alert('draw');
                    }
                }
                $scope.currentPlayer = 1;
            }).error(function (data, status, headers, config) {
                alert(data);
            });
        }
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
    this.gameBoard = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];
    this.makeMove = function (col, row, player) {
        if (this.gameBoard[col][row] === 0) {
            this.gameBoard[col][row] = player;
            return true;
        }
        else return false;
    };
}