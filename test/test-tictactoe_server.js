
var tttoe = require('../lib/tictactoeserver');


/**
 * @desc Unit test for isGameOver()
 */
exports['isGameOver'] = function (test) {
  var x = getBoardStateSample();
  var result = tttoe.isGameOver(x);

  console.log('x:');
  console.log(x);
  console.log('result:');
  console.log(result);

  test.equal(result.gameOver, false);
  test.done();
};
