var tic = angular
        .module('tictac', [])
        .config(
                [
                        '$compileProvider',
                        function($compileProvider) {
                            $compileProvider
                                    .aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);
                        } ]);

tic
        .controller(
                'game',
                function($scope) {

                    $scope.currentPlayer = 'X';
                    $scope.player = 'X';
                    $scope.winner = null;
                    $scope.board = [ [ null, null, null ],
                            [ null, null, null ], [ null, null, null ] ];

                    var keys = [ 'board', 'currentPlayer', 'winner' ];

                    $scope.cellClass = function(row, column) {
                        var value = cell(row, column);
                        return 'cell cell-' + value;
                    }
                    $scope.cellText = function(row, column) {
                        var value = cell(row, column);
                        return value ? value : '-';
                    }
                    $scope.cellClick = function(row, column) {
                        if ($scope.winner) {
                            alert('WINNER!!');
                            return;
                        }
                        if ($scope.player != $scope.currentPlayer) {
                            alert('Waiting for other player to complete their turn.');
                            return;
                        }

                        var set = setCell(row, column, $scope.player);
                        checkBoard();

                        if (set) {
                            $scope.currentPlayer = nextPlayer($scope.currentPlayer);
                        }
                    }
                    $scope.newGame = function() {
                        for (var i = 0; i < 3; i++) {
                            for (var j = 0; j < 3; j++) {
                                setCell(i, j, null);
                            }
                        }
                        $scope.currentPlayer = 'X';
                        $scope.player = 'X';
                        $scope.winner = null;
                        $scope.board = [ [ null, null, null ],
                                [ null, null, null ], [ null, null, null ] ];

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
                        console.log($scope.board[row][column]);
                        if ($scope.board[row][column] == null) {
                            $scope.board[row][column] = value;
                            return true;
                        }
                        return false;
                    }

                    /**
                     * 
                     */
                    function nextPlayer(player) {
                        return {
                            O : 'X',
                            X : 'O'
                        }[player];
                    }

                    /**
                     * 
                     */
                    function request(board) {
                        $http
                                .get(
                                        '/')
                                .success(function(data) {

                                    // verify instances were found
                                    if (data.length > 0) {
                                        store.buildChecked(data);
                                    }

                                }).error(function(data) {
                                    // console.log('Error: --' + data);
                                });

                    }
                    /**
                     * 
                     */
                    function checkBoard() {
                        var winner, empty = false;

                        // check for any empty cell
                        for (var i = 0; i < 3; i++) {
                            for (var j = 0; j < 3; j++) {
                                if (!cell(i, j)) empty = true;
                            }
                        }

                        // no more empty cell - no winner
                        if (!empty) {
                            $scope.winner = 'NONE';
                            return;

                        }

                        // check board vertically and horizontally
                        for (var i = 0; i < 3; i++) {
                            if (cell(i, 0) && cell(i, 0) == cell(i, 1)
                                    && cell(i, 1) == cell(i, 2)) {
                                winner = cell(i, 0);
                            }
                            if (cell(0, i) && cell(0, i) == cell(1, i)
                                    && cell(1, i) == cell(2, i)) {
                                winner = cell(0, i);
                            }
                        }

                        // check board diagonally
                        if (cell(0, 0) && cell(0, 0) == cell(1, 1)
                                && cell(1, 1) == cell(2, 2)) {
                            winner = cell(0, 0);
                        }
                        if (cell(0, 2) && cell(0, 2) == cell(1, 1)
                                && cell(1, 1) == cell(2, 0)) {
                            winner = cell(0, 2);
                        }

                        // winner? declare!
                        if (winner) {
                            $scope.winner = winner;
                        }

                    }

                });
