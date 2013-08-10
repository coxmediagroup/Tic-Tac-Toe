(function () {

  var botDelay = 0;
  var resetDelay = 1000;
  var currentPlayer = null;
  var waitingPlayer = null;
  var player1 = null;
  var player2 = null;

  function Player(number, symbol, el, isHuman) {
    this.number = number;
    this.symbol = symbol;
    this.el = el;
    this.isHuman = isHuman === undefined ? true : false;
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
      this._elDraws.innerHTML = this.draws;
      if (this === currentPlayer) waitingPlayer.addDraw();
    },
    startTurn: function () {
      if (currentPlayer) currentPlayer.el.className = '';
      board.el.className = 'turn-player' + this.number;
      waitingPlayer = this === player1 ? player2 : player1;
      currentPlayer = this;
      currentPlayer.el.className = 'current';
      if (!this.isHuman) {
        // if the bot is going first, randomize the start position
        console.log(board.turns);
        if (board.turns === 0) {
          board.mark(Math.floor(Math.random() * 9));
        } else {
          setTimeout(function () {
            board.mark(sim.minimax(2)[1]);
          }, botDelay);
        }
      }
    }
  };

  var board = window.board = {
    el: document.getElementById('board'),
    turns: 0,
    marks: new Array(9),

    // current player adds their marks at index
    mark: function (index, el) {
      console.log(index);
      el = el || board.el.children[index];
      el.innerHTML = currentPlayer.symbol;
      el.className = 'marked player' + currentPlayer.number;
      board.marks[index] = currentPlayer.number;
      board.turns += 1;
      win = sim.getWin();
      if (win) {
        currentPlayer.addWin();
        for (var i=3; i--;)
          board.el.children[win[i]].className += ' winner';
        setTimeout(function () {
          board.reset();
        }, resetDelay);
      } else if (this.turns === 9) {
        currentPlayer.addDraw();
        for (var i=9; i--;)
          board.el.children[i].className += ' draw';
        setTimeout(function () {
          board.reset();
        }, resetDelay);
      } else {
        waitingPlayer.startTurn();
      }
    },
    reset: function () {
      board.turns = 0;
      board.marks = new Array(9);
      for (var i=board.el.children.length; i--;) {
        board.el.children[i].className =
        board.el.children[i].innerHTML = '';
      }
      player1.startTurn();
    },
    corners: [0, 2, 6, 8],
    sides: [1, 3, 5, 7],
    wins: [
      [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
      [0, 3, 6], [1, 4, 7], [2, 5, 8], // cols
      [0, 4, 8], [2, 4, 6] // diagonals
    ]
  };

  var sim = {
    minimax: function (depth, player) {
      player = player || currentPlayer;
      var bestScore = player === currentPlayer ? -Infinity : Infinity;
      var bestPosition = -1;
      var available = [];
      var currentScore, i;

      for (i=9; i--;)
        if (!board.marks[i]) available.push(i);

      if (!available.length || !depth) {
        // Gameover or depth reached, evaluate score
        bestScore = sim.evaluate();
      } else {
        for (i=available.length; i--;) {
          var index = available[i];
          board.marks[index] = player.number;
          if (player === currentPlayer) {  // max
            currentScore = sim.minimax(depth - 1, waitingPlayer)[0];
            if (currentScore > bestScore) {
              bestScore = currentScore;
              bestPosition = index;
            }
          } else {  // min
            currentScore = sim.minimax(depth - 1, currentPlayer)[0];
            if (currentScore < bestScore) {
              bestScore = currentScore;
              bestPosition = index;
            }
          }
          board.marks[index] = null; // Undo move
        }
      }
      return [bestScore, bestPosition];
    },
    _filter: function (player) {
      return function (playerNumber) { return playerNumber === player.number; };
    },
    // give the current board a score in how desirable it is
    evaluate: function () {
      var score = 0;
      for (var i=board.wins.length; i--;) {
        var win = board.wins[i];
        var marks = [board.marks[win[0]], board.marks[win[1]],
                     board.marks[win[2]]];
        var currentPlayerCount = marks.filter(sim._filter(currentPlayer)).length;
        var waitingPlayerCount = marks.filter(sim._filter(waitingPlayer)).length;

        if (currentPlayerCount && waitingPlayerCount)
          continue;

        if (currentPlayerCount === 3)
          score += 100;
        else if (currentPlayerCount === 2)
          score += 10;
        else if (currentPlayerCount === 1)
          score += 1;

        if (waitingPlayerCount === 3)
          score -= 100;
        else if (waitingPlayerCount === 2)
          score -= 10;
        else if (waitingPlayerCount === 1)
          score -= 1;
      }
      return score;
    },
    getWin: function () {
      for (var i=board.wins.length; i--;) {
        for (var z=3; z--;) {
          if (board.marks[board.wins[i][z]] !== currentPlayer.number) break;
          if (z === 0) return board.wins[i];
        }
      }
      return false;
    }
  };


  player1 = new Player(1, '×', document.getElementById('player1'), false);
  player2 = new Player(2, '○', document.getElementById('player2'));

  board.reset();

  board.el.addEventListener('click', function (e) {
    // disallow humans to make marks while computer is thinking
    if (!currentPlayer.isHuman || e.target.className.indexOf('marked') !== -1)
      return;
    //var x = index % 3, y = Math.floor(index / 3);
    board.mark(Array.prototype.indexOf.call(this.children, e.target), e.target);
  });

}());
