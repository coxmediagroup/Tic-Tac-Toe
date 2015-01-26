

//var assert = require('assert');

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
exports.getBoardStateSample = function() {
  var x = null;
  //x = [['X', '', ''], ['', 'X', ''], ['', '', 'X']];
  x = [['O', '', ''], ['', 'X', ''], ['', '', 'X']];
  //x = [['', '', ''], ['', '', ''], ['', '', '']]; // An empty board.
  return x;
}



/**
 * @desc Define a function that takes a board state as input and decides
 *    whether a player has one.
 * INPUT:
 *   boardState: 2-dimensional array
 * OUTPUT:
 *   {
 *      gameOver: false or true,
 *      player: blank or X or O 
 *   }
 */
//function isGameOver(x) {
exports.isGameOver = function (x) {
  var playerWinner = '';
  var result = {};
  result['gameOver'] = false;
  //result["player"] = 'X';
  if ((x[0][0] != '') && (x[0][0] == x[1][1]) && (x[1][1] == x[2][2])) {
    result['gameOver'] = true;
    playerWinner = x[0][0];
  }
  result['player'] = playerWinner;
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
//function getMPAvailableMoves(x) {
exports.getMPAvailableMoves = function(x) {
  var remainMoves = [];
  var blank = '';
  for (i =0; i<3; i++) {
    for (j =0; j<3; j++) {
      if (x[i][j] == blank) {
        remainMoves.push([i,j]);
      }
    }
  }
  return remainMoves;
}

/**
* @desc Returns a random move. Assumes the player symbol is 'X'.
*/
exports.getMPNextMoveRandom = function(x) {
  var remainMoves = exports.getMPAvailableMoves(x);
  var indexMove = exports.getNumRandomInteger(0, remainMoves.length);
  var xmove = remainMoves[indexMove];

  var nextMove = {};
  nextMove['moveLocation'] = xmove;
  nextMove['playerSymbol'] = 'X';
  return nextMove;
}


/**
 * param Array x
 * @desc Given a current board state, update it using nextMove. Return the updated board. Note: You cannot update a cell that already as a value. If this happens, the function will throw an error.
 */
exports.updateBoard = function(x, nextMove) {
  var mLoc = nextMove['moveLocation'];
  var pSymbol = nextMove['playerSymbol'];
  x[mLoc[0]][mLoc[1]] = pSymbol;
  return x;
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


