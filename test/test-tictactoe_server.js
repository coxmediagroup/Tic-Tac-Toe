
var t = require('../lib/tictactoeserver');


/**
 * @desc Unit test for isGameOver()
 */
exports['getGameState'] = function (test) {
  var board = null; 
  var gstate = null; 

  var blank = ''
  console.log('board:');
  console.log(board);
  console.log('gstate:');
  console.log(gstate);

  board = t.getBoardStateSample('initial');
  gstate = t.getGameState(board);
  test.equal(gstate.isGameOver, false);
  test.equal(gstate.playerWinner, blank);

  board = t.getBoardStateSample('a');
  gstate = t.getGameState(board);
  test.equal(gstate.isGameOver, true);
  test.equal(gstate.playerWinner, 'X');

  board = t.getBoardStateSample('b');
  gstate = t.getGameState(board);
  test.equal(gstate.isGameOver, true);
  test.equal(gstate.playerWinner, 'O');

  board = t.getBoardStateSample('c');
  gstate = t.getGameState(board);
  test.equal(gstate.isGameOver, true);
  test.equal(gstate.playerWinner, 'draw');

  test.done();
};
