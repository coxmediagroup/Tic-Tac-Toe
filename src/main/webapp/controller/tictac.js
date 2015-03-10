/**
 * 
 */
var tictac = angular
        .module('tictac', [])
        .config(
                [
                        '$compileProvider',
                        function($compileProvider) {
                            $compileProvider
                                    .aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);
                        } ]);

/**
 * 
 */
tictac.controller('play', function($scope, $http) {

    $scope.b = ' ';

    $scope.currentPlayer = 'X';
    $scope.player = 'X';
    $scope.winner = null;
    $scope.board = [ [ null, null, null ], [ null, null, null ],
            [ null, null, null ] ];

    $scope.firstMove = true;
    var keys = [ 'board', 'currentPlayer', 'winner' ];

    /**
     * 
     */
    $scope.cellClass = function(row, column) {
        var value = cell(row, column);
        return 'cell cell-' + value;
    }

    /**
     * 
     */
    $scope.cellText = function(row, column) {
        var value = cell(row, column);
        return value ? value : '-';
    }

    /**
     * 
     */
    $scope.cellClick = function(row, column) {

        console.log('row: ' + row + '-Column: ' + column + '-Current Player '
                + $scope.currentPlayer);

        var set = setCell(row, column, $scope.player);

        if (!set) return;

        console.log('Do AI stuff');

        var payload = {
            'firstMove' : $scope.firstMove,
            'board' : $scope.board
        };

        checkWin('/checkboard', arrayToJSON($scope.board));

        ai('/automate', payload);

        // after first pass set to false
        if ($scope.firstMove) {
            $scope.firstMove = false;
        }

    }

    /**
     * 
     */
    function arrayToJSON(array) {
        console.log(JSON.stringify(array));
        return JSON.stringify(array);
    }

    /**
     * 
     */
    function jsonToArray(json) {
        console.log(JSON.parse(json));
        return JSON.parse(json);
    }

    /**
     * 
     */
    $scope.newGame = function() {
        for (var i = 0; i < 3; i++) {
            for (var j = 0; j < 3; j++) {
                setCell(i, j, null);
            }
        }
        $scope.currentPlayer = 'X';
        $scope.player = 'X';
        $scope.winner = null;
        $scope.board = [ [ null, null, null ], [ null, null, null ],
                [ null, null, null ] ];
        $scope.firstMove = true;
    }

    /**
     * 
     */
    function cell(row, column) {
        return $scope.board[row][column];
    }

    /**
     * 
     */
    function setCell(row, column, value) {

        if ($scope.board[row][column] == null) {
            $scope.board[row][column] = value;
            return true;
        }
        return false;
    }

    /**
     * REST HANDLER
     */
    function checkWin(endpoint, payload) {

        $http.post(endpoint, payload).success(function(data) {

            if (data == 'tie') {
                $scope.winner = 'NO ONE';
                alert('tie');
                return;
            } else {
                if (data == 'X' || data == 'O') {

                    $scope.winner = data;
                    alert('WINNER!!');
                    return;
                }
            }
        }).error(function(data) {
            console.log('Error: --' + data);
        });

    }

    /**
     * REST HANDLER
     */
    function ai(endpoint, payload) {

        $http.post(endpoint, payload).success(function(data) {

            // return board with O move
            $scope.board = jsonToArray(JSON.stringify(data));
            console.log("AI RESPONSE: " + data);
        }).error(function(data) {
            console.log('Error: --' + data);
        });

    }

});
