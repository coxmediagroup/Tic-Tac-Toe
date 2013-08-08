(function () {

  var $ = document.querySelectorAll.bind(document);
  var elContainer = $('#container')[0];
  var elBoard = $('#board')[0];
  var players = [
    { symbol: '×', w: 0, l: 0, d: 0, el: $('#player1')[0], isHuman: true },
    { symbol: '○', w: 0, l: 0, d: 0, el: $('#player2')[0], isHuman: true }
  ];
  var player = 0;
  var board = [[], [], []];

  elBoard.addEventListener('click', function (e) {
    if (!players[player].isHuman || e.target.className.indexOf('marked') !== -1)
      return;
    mark(e.target);
  });

  function mark(elSquare) {
    var index = Array.prototype.indexOf.call(elBoard.children, elSquare);
    var coords = locate(index);
    elSquare.innerHTML = board[coords.x][coords.y] = players[player].symbol;
    elSquare.className = 'marked player' + (player + 1);
    players[player].el.className = '';
    player = player === 0 ? 1 : 0;
    elContainer.className = 'turn-player' + (player + 1);
  }

  // Gets coordinates from the index
  function locate(index) {
    return { x: Math.floor(index / board.length), y: index % board.length };
  }

  function findWins(lastMark) {

  }

}());
