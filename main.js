(function () {

  function Player(symbol, el, isHuman) {
    this.symbol = symbol;
    this.el = el;
    this.isHuman = isHuman || true;
    this.wins = 0;
    this.losses = 0;
    this.draws = 0;
    this._elWins = el.children[1];
    this._elLosses = el.children[2];
    this._elDraws = el.children[3];
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
    },
    addLoss: function () {
      this.losses++;
      this._elLosses.innerHTML = this.losses;
    },
    addDraw: function () {
      this.draws++;
      this._elDraws.innerHTML = this.elDraws;
    }
  };

  function Board(el, size) {
    this.el = el;
    this.size = size || 3;
    this.players = [
      new Player('&times;', document.getElementById('player1')),
      new Player('○', document.getElementById('player2'))
    ];
    this.reset();

    var _this = this;
    this.el.addEventListener('click', function (e) {
      if (!_this.players[_this.currentPlayer].isHuman ||
          e.target.className.indexOf('marked') !== -1)
        return;
      _this.mark(Array.prototype.indexOf.call(this.children, e.target));
    });
  }

  Board.prototype = {
    mark: function (index) {
      var square = this.el.children[index];
      square.innerHTML = this.players[this.currentPlayer].symbol;
      square.className = 'marked player' + (this.currentPlayer + 1);
      this.squares[index] = this.currentPlayer;
      this.turns += 1;
      if (this.isWinningMove(index)) {
        this.players[this.currentPlayer].addWin();
        this.players[this.currentPlayer === 0 ? 1 : 0].addLoss();
        this.reset();
      } else if (this.turns === board.length) {
        this.players[0].addDraw();
        this.players[1].addDraw();
        this.reset();
      } else {
        this.next();
      }
    },
    next: function (index) {
      this.currentPlayer = index ? index : this.currentPlayer === 0 ? 1 : 0;
      this.players[this.currentPlayer].el.className = '';
      document.getElementById('container').className = 'turn-player' + (this.currentPlayer + 1);
    },
    reset: function () {
      console.log('reset');
      this.currentPlayer = 0;
      this.turns = 0;
      this.squares = new Array(this.size^2);
      for (var i=this.el.children.length; i--;) {
        var square = this.el.children[i];
        square.className = square.innerHTML = '';
      }
    },
    isWinningMove: function (index) {
      var x = index % this.size, y = Math.floor(index / this.size);

      // check for win at col
      for (var i=this.size; i--;) {
        if (this.squares[i * this.size + x] !== this.currentPlayer) break;
        if (i === 0) return true;
      }

      // check for win at row
      for (var i=this.size; i--;) {
        if (this.squares[y * this.size + i] !== this.currentPlayer) break;
        if (i === 0) return true;
      }

      // check for diagonal win
      if (x === y) {
        for (var i=this.size; i--;) {
          if (this.squares[i * (this.size + 1)] !== this.currentPlayer) break;
          if (i === 0) return true;
        }
      }

      // check for anti-diagonal
      for (var i=this.size; i--;) {
        var t = (i + 1) * (this.size - 1);
        if (this.squares[(i + 1) * (this.size - 1)] !== this.currentPlayer) break;
        if (i === 0) return true;
      }

      return false;
    }
  };

  window.onload = function () {
    var board = new Board(document.getElementById('board'));
  };


}());
