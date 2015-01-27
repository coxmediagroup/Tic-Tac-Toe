

//var assert = require('assert');

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
//exports.getBoardStateSample = function() {
//  var x = null;
//  //x = [['X', '', ''], ['', 'X', ''], ['', '', 'X']];
//  x = [['O', '', ''], ['', 'X', ''], ['', '', 'X']];
//  //x = [['', '', ''], ['', '', ''], ['', '', '']]; // An empty board.
//  return x;
//}

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



  var playerPrevious = '';
  board.data = x;
  board.playerPrevious = playerPrevious;
  return board;
}



/**
 * @desc Define a function that takes a board state as input and decides
 *    whether a game is complete.
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

  var remainMoves = exports.getMPAvailableMoves(board.data);


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
 * @param {Array} x Current tic-tac-toe board state.
 * @desc Given a board state, get the machine player's next move. THe algorithm is that of a perfect player as described in the wiki article.
 * @output JSON nextMove {moveLocation:[], playerSymbol:'X'}
 */
exports.getMPNextMove = function(x) {
  var nextMove = {}
  nextMove['moveLocation'] = [1,0];
  nextMove['playerSymbol'] = 'X';
  return nextMove;
}


/**
* For a given board state, return availble moves for player 'X'.
*/
exports.getMPAvailableMoves = function(x) {
  console.log('from getMPAvailbleMoves');
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
  console.log('From remainMoves');
  console.log(remainMoves);
  return remainMoves;
}

/**
* @desc Returns a random move. Assumes the player symbol is 'X'.
*/
exports.getMPNextMoveRandom = function(board) {
  var remainMoves = exports.getMPAvailableMoves(board.data);
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

// Get an intial board.
//var x = getBoardStateSample();
//var x = {};
//console.log(x);

// Check whether a player won or draw.
//var result = isGameOver(x);
//var result = {};
//console.log(result);

// Get next move.
//var nextMove = getMPNextMove(x);
//console.log(nextMove);

// Update the board with the move:
//x = updateBoard(x, nextMove);
//console.log(x);


