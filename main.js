(function () {

  var elBoard = document.getElementById('board');
  var isThinking = false;
  var x = '×', o = '○';
  var board = [[], [], []];
  var size = 3;

  elBoard.addEventListener('click', function (e) {
    if (isThinking || e.target.className === 'marked') return;
    var index = Array.prototype.indexOf.call(elBoard.children, e.target);
    var x = Math.floor(index / size);
    var y = index % size;
    e.target.innerHTML = o;
    e.target.className = 'marked';
    board[x][y] = o;
    move(x, y);
  });

  function move(x, y) {
  }

}());
