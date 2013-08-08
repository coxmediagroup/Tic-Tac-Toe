(function () {

  // for simple native jquery-style code
  var $ = document.querySelectorAll.bind(document);
  Element.prototype.on = Element.prototype.addEventListener;

  var elBoard = $('#board')[0];
  var player1 = { symbol: '×', w: 0, l: 0, d: 0, el: $('#player1')[0], isHuman: true },
      player2 = { symbol: '○', w: 0, l: 0, d: 0, el: $('#player2')[0], isHuman: true };
  var currentPlayer = player1;
  var board = [[], [], []];

  elBoard.on('click', function (e) {
    if (!currentPlayer.isHuman || e.target.className === 'marked') return;
    mark(e.target);
  });

  function mark(elSquare) {
    var index = Array.prototype.indexOf.call(elBoard.children, elSquare);
    var coords = locate(index);
    elSquare.innerHTML = board[coords.x][coords.y] = currentPlayer.symbol;
    elSquare.className = 'marked';
    currentPlayer.el.className = '';
    currentPlayer = currentPlayer === player1 ? player2 : player1;
    currentPlayer.el.className = 'current';
  }

  // Gets coordinates from the index
  function locate(index) {
    return { x: Math.floor(index / board.length), y: index % board.length };
  }

}());
