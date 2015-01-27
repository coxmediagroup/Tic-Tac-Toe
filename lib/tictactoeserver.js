


var pSymbolMap = {human:'X', machine:'O'};

/**
 * @desc Utility: Generate a rando number for a given range.
 */
exports.getNumRandomInteger = function(xBegin, xEnd) {
  var rangeSize = xEnd - xBegin;
  var numRandomInt = Math.floor(Math.random() * rangeSize);
  numRandomInt = numRandomInt + xBegin;
  return numRandomInt;
}

/**
 * @desc Returns a tic-tac-toe board state for testing purpose.
 */
exports.getBoardStateSample = function(btype) {
  var board = {};
  var x = null;
  if (btype == 'initial') {
    x = [['', '', ''], ['', '', ''], ['', '', '']]; // An empty board.
  }
  if (btype == 'a') {
    x = [['X', '', ''], ['', 'X', ''], ['', '', 'X']]; // Player 'X' wins.
  }
  if (btype == 'b') {
    x = [['', '', 'O'], ['', 'O', ''], ['O', '', '']]; // Player 'O' wins.
  }
  if (btype == 'c') {
    x = [['O', 'X', 'O'], ['O', 'X', 'O'], ['X', 'O', 'X']]; // draw.
  }
  if (btype == 'd') {
    x = [['O', 'X', 'O'], ['O', 'X', 'O'], ['', 'X', '']]; // X wins.
  }

  var playerPrevious = '';
  board.data = x;
  board.playerPrevious = playerPrevious;
  return board;
}



/**
 * @desc Define a function that takes a board state as input and decides
 *    whether a game is over.
 * INPUT:
 *   boardState: 2-dimensional array
 * OUTPUT:
 *   {
 *      isGameOver: false, true
 *      playerWinner: '', draw, human, machine
 *   }
 */
exports.getGameState = function (board) {
  var x = board.data;
  var playerWinner = '';
  var result = {};

  var remainMoves = exports.getAvailableMoves(board.data);


  result.isGameOver = false;
  result.playerWinner = '';

  //result["player"] = 'X';
  if ((x[0][0] != '') && (x[0][0] == x[1][1]) && (x[1][1] == x[2][2])) {
    result.isGameOver = true;
    result.playerWinner = x[0][0];
  } else if ((x[2][0] != '') && (x[2][0] == x[1][1]) && (x[1][1] == x[0][2])) {
    result.isGameOver = true;
    result.playerWinner = x[2][0];

  } else if ((x[0][0] != '') && (x[0][0] == x[0][1]) && (x[0][1] == x[0][2])) {
    result.isGameOver = true;
    result.playerWinner = x[0][0];
  } else if ((x[1][0] != '') && (x[1][0] == x[1][1]) && (x[1][1] == x[1][2])) {
    result.isGameOver = true;
    result.playerWinner = x[1][0];
  } else if ((x[2][0] != '') && (x[2][0] == x[2][1]) && (x[2][1] == x[2][2])) {
    result.isGameOver = true;
    result.playerWinner = x[2][0];

  } else if ((x[0][0] != '') && (x[0][0] == x[1][0]) && (x[1][0] == x[2][0])) {
    result.isGameOver = true;
    result.playerWinner = x[0][0];
  } else if ((x[0][1] != '') && (x[0][1] == x[1][1]) && (x[1][1] == x[2][1])) {
    result.isGameOver = true;
    result.playerWinner = x[0][1];
  } else if ((x[0][2] != '') && (x[0][2] == x[1][2]) && (x[1][2] == x[2][2])) {
    result.isGameOver = true;
    result.playerWinner = x[0][2];

  } else if (remainMoves.length == 0) {
    result.isGameOver = true;
    result.playerWinner = 'draw';
  }

  return result;
}




/**
 * @desc Returns a list of locations to check on the board.
 */
exports.getCellLocList = function() {
  var xyList = [];
  xyList.push([[0,0], [0,1], [0,2]]);
  xyList.push([[1,0], [1,1], [1,2]]);
  xyList.push([[2,0], [2,1], [2,2]]);

  xyList.push([[0,0], [1,0], [2,0]]);
  xyList.push([[0,1], [1,1], [2,1]]);
  xyList.push([[0,2], [1,2], [2,2]]);

  xyList.push([[0,0], [1,1], [2,2]]);
  xyList.push([[2,0], [1,1], [0,2]]);
  return xyList;
}

/**
 * @desc First step of the perfect player.
 */
exports.getMoveListWin = function(board) {
  var blank = '';
  var x = board.data;
  var moveList = [];
  var ma = null;
  var mb = null;
  var mc = null;
  cellLocList = exports.getCellLocList();
  for (i=0; i<cellLocList.length; i++) {
    ma = cellLocList[i][0];
    mb = cellLocList[i][1];
    mc = cellLocList[i][2];

    if ((x[ma[0]][ma[1]] == 'O') && (x[mb[0]][mb[1]] == 'O') && (x[mc[0]][mc[1]] == blank)) {
      moveList.push(mc);
    } else if ((x[ma[0]][ma[1]] == blank) && (x[mb[0]][mb[1]] == 'O') && (x[mc[0]][mc[1]] == 'O')) {
      moveList.push(ma);
    }
  }
  return moveList;
}

/**
 * @desc Second step of the perfect player.
 */
exports.getMoveListBlock = function(board) {
  var blank = '';
  var x = board.data;
  var moveList = [];
  var ma = null;
  var mb = null;
  var mc = null;
  cellLocList = exports.getCellLocList();
  for (i=0; i<cellLocList.length; i++) {
    ma = cellLocList[i][0];
    mb = cellLocList[i][1];
    mc = cellLocList[i][2];

    if ((x[ma[0]][ma[1]] == 'X') && (x[mb[0]][mb[1]] == 'X') && (x[mc[0]][mc[1]] == blank)) {
      moveList.push(mc);
    } else if ((x[ma[0]][ma[1]] == blank) && (x[mb[0]][mb[1]] == 'X') && (x[mc[0]][mc[1]] == 'X')) {
      moveList.push(ma);
    }
  }
  return moveList;
}

/**
 * @desc Third step of the perfect player.
 */
exports.getMoveListFork = function(board) {
  var blank = '';
  var x = board.data;
  var moveList = [];
  var ma = null;
  var mb = null;
  var mc = null;
  cellLocList = exports.getCellLocList();
  for (i=0; i<cellLocList.length; i++) {
    ma = cellLocList[i][0];
    mb = cellLocList[i][1];
    mc = cellLocList[i][2];

    if ((x[ma[0]][ma[1]] == 'O') && (x[mb[0]][mb[1]] == blank) && (x[mc[0]][mc[1]] == blank)) {
      moveList.push(mb);
    } else if ((x[ma[0]][ma[1]] == blank) && (x[mb[0]][mb[1]] == 'O') && (x[mc[0]][mc[1]] == blank)) {
      moveList.push(ma);
      moveList.push(mc);
    } else if ((x[ma[0]][ma[1]] == blank) && (x[mb[0]][mb[1]] == blank) && (x[mc[0]][mc[1]] == 'O')) {
      moveList.push(mb);
    }
  }
  return moveList;
}


/**
* @desc For a given board state, return availble moves..
*/
exports.getAvailableMoves = function(x) {
  console.log('from getAvailbleMoves');
  console.log(x);

  var remainMoves = [];
  var blank = '';
  for (i =0; i<3; i++) {
    for (j =0; j<3; j++) {
      if (x[i][j] == blank) {
        remainMoves.push([i,j]);
      }
    }
  }
  //console.log('From remainMoves');
  //console.log(remainMoves);
  return remainMoves;
}

/**
* @desc Returns a random move. Assumes the player symbol is 'X'.
*/
exports.getMachineNextMoveSimple = function(board) {
  var remainMoves = exports.getAvailableMoves(board.data);
  var indexMove = exports.getNumRandomInteger(0, remainMoves.length);
  //var xmove = remainMoves[indexMove];
  var xmove = remainMoves[0];  // Not random.
  var cellIdx = xmove[0]*3 + xmove[1] + 1;
  var nextMove = {};
  nextMove['cellIdx'] = cellIdx;
  nextMove['player'] = 'machine';
  return nextMove;
}

/**
 * 
 * @desc Given a board state, get the machine player's next move. THe algorithm is that of a perfect player as described in the tic-tac-toe wiki article (http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy), which references the following article:
 * Kevin Crowley, Robert S. Siegler (1993). "Flexible Strategy Use in Young Children’s Tic-Tac-Toe". Cognitive Science 17 (4): 531–561
 * @output JSON nextMove {cellIdx:integer, player: [human, machine]}
 */
exports.getMachineNextMove = function(board) {
  var nextMove = {}
  var moveListWin = exports.getMoveListWin(board);
  var moveListBlock = exports.getMoveListBlock(board);
  var moveListFork = exports.getMoveListFork(board);
  var xmove = null;

  if (moveListWin.length > 0) {     // 1) WIN: Making this will win the game for the machine.
    xmove = moveListWin[0];
  } else if (moveListBlock.length > 0) {
    xmove = moveListBlock[0];
  } else if (moveListFork.length > 0) {
    xmove = moveListFork[0];
  } 
  else { // Rely on the simple move algorithm.
    var remainMoves = exports.getAvailableMoves(board.data);
    xmove = remainMoves[0];
  }

  var cellIdx = xmove[0]*3 + xmove[1] + 1;
  nextMove['cellIdx'] = cellIdx;
  nextMove['player'] = 'machine';
  return nextMove;
}


/**
 * param Array x
 * @desc Given a current board state, update it using nextMove. Return the updated board. Note: You cannot update a cell that already as a value. If this happens, the function will throw an error.
 */
exports.updateBoard = function(board, nmove) {
  var i = 0;
  var j = 0;
  i = Math.floor((nmove.cellIdx-1)/3)
  j = (nmove.cellIdx - 1) % 3;
  board.data[i][j] = pSymbolMap[nmove.player];
  board.playerBefore = nmove.player;  

  // Determine whether a game is complete: [draw, humanWins, machineWins]
  return board;
}

