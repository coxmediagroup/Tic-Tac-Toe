(function () {

  var currentPlayer = null;
  var waitingPlayer = null;
  var player1 = null;
  var player2 = null;

  function Player(number, symbol, el, isHuman) {
    console.log(this);
    this.number = number;
    this.symbol = symbol;
    this.el = el;
    this.isHuman = isHuman || true;
    this._elWins = el.children[1];
    this._elLosses = el.children[2];
    this._elDraws = el.children[3];
    this.reset();
  }

  Player.prototype = {
    reset: function () {
      this.wins =
      this.losses =
      this.draws =
      this._elWins.innerHTML =
      this._elLosses.innerHTML =
      this._elDraws.innerHTML = 0;
    },
    addWin: function () {
      this.wins++;
      this._elWins.innerHTML = this.wins;
      waitingPlayer.addLoss();
    },
    addLoss: function () {
      this.losses++;
      this._elLosses.innerHTML = this.losses;
    },
    addDraw: function () {
      this.draws++;
      this._elDraws.innerHTML = this.elDraws;
      waitingPlayer.addDraw();
    },
    startTurn: function () {
      if (currentPlayer) currentPlayer.el.className = '';
      board.el.className = 'turn-player' + this.number;
      waitingPlayer = this === player1 ? player2 : player1;
      currentPlayer = this;
      currentPlayer.el.className = 'current';
      if (!this.isHuman) console.log('simulate');
    }
  };

  var board = {
    el: document.getElementById('board'),
    mark: function (x, y, el) {
      el.innerHTML = currentPlayer.symbol;
      el.className = 'marked player' + currentPlayer.number;
      board.marks[x][y] = currentPlayer.number;
      board.turns += 1;
      if (board.isWin(x, y)) {
        currentPlayer.addWin();
        board.reset();
      } else if (this.turns === 9) {
        currentPlayer.addDraw();
        board.reset();
      } else {
        waitingPlayer.startTurn();
      }
    },
    reset: function () {
      player1.startTurn();
      board.turns = 0;
      board.marks = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]];
      for (var i=board.el.children.length; i--;) {
        board.el.children[i].className =
        board.el.children[i].innerHTML = '';
      }
    },
    isWin: function (x, y) {
      var i, square;

      // check for win at col
      for (i=3; i--;) {
        if (board.marks[x][i] !== currentPlayer.number) break;
        if (i === 0) return true;
      }

      // check for win at row
      for (i=3; i--;) {
        if (board.marks[i][y] !== currentPlayer.number) break;
        if (i === 0) return true;
      }

      // check for diagonal win
      if (x === y) {
        for (i=3; i--;) {
          if (board.marks[i][i] !== currentPlayer.number) break;
          if (i === 0) return true;
        }
      }

      // check for anti-diagonal
      for (i=3; i--;) {
        if (board.marks[i][2 - i] !== currentPlayer.number) break;
        if (i === 0) return true;
      }

      return false;
    }

  };

  player1 = new Player(1, '×', document.getElementById('player1'));
  player2 = new Player(2, '○', document.getElementById('player2'));

  board.reset();
  board.el.addEventListener('click', function (e) {
    // disallow humans to make marks while computer is thinking
    if (!currentPlayer.isHuman || e.target.className.indexOf('marked') !== -1)
      return;
    var index = Array.prototype.indexOf.call(this.children, e.target);
    var x = index % 3, y = Math.floor(index / 3);
    board.mark(x, y, e.target);
  });

}());
