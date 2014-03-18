/* global define */
define([
  'underscore',
  'backbone',
  'app-base',
  'backbone-layout',
  'apps/tic-tac-toe/views/header',
  'apps/tic-tac-toe/views/game-main',
  'apps/tic-tac-toe/views/footer',
  'apps/tic-tac-toe/views/game-over'
], function(_, Backbone, AppBase, Layout, Header, Game, Footer, GameOver) {
  'use strict';

  // MainLayout
  // ---------

  // The main layout for the game. This isn't the game itself. Instead, this is
  // the scaffolding upon which the game views will be rendered.
  var MainLayout = Layout.extend({
    className: 't3-game',

    template: _.template(
      '<div class="game-header"></div>' +
      '<div class="game-view"></div>' +
      '<div class="game-footer"></div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);

      this.header = new Header({ model: this.options.stats });
      this.game = new Game({
        state: this.options.state,
        players: this.options.players
      });
      this.footer = new Footer({ model: this.options.state });

      this.registerView(this.header, {anchor: '.game-header', replace: true});
      this.registerView(this.game, {anchor: '.game-view', replace: true});
      this.registerView(this.footer, {anchor: '.game-footer', replace: true});
    }
  });

  // Player
  // ------

  // A model representing a specific player (human or computer).
  var Player = Backbone.Model.extend({
    initialize: function() {
      this.taken = [false,  // Ignore 0 index
                    false, false, false,
                    false, false, false,
                    false, false, false];

      this.pairs = [false, false, false, false,
                    false, false, false, false,
                    false, false, false, false,
                    false, false, false, false];
    },

    updatePairs: function(cellId) {
      for (var i = 1; i <= 9; i++) {
        if (this.taken[i] && i + cellId < 15) {
          this.pairs[cellId + i] = true;
        }
      }
    },

    deepClone: function() {
      var clone = this.clone();
      clone.taken = _.clone(this.taken);
      clone.pairs = _.clone(this.pairs);
      return clone;
    }
  });

  // T3App
  // -----

  // This is in charge of the Tic-Tac-Toe application. It tracks the state
  // changes that relate to the 't3' namespace and it is responsible for the
  // game logic.
  var T3App = AppBase.extend({
    // ##initialize
    initialize: function(options) {
      this.layoutManager = options.layoutManager;
      this.state = options.state;
      this.listenTo(this.state, 'change:name', this.onChangeState);

      // Record some basic game stats
      this.stats = new (Backbone.Model.extend({
        defaults: {
          gamesPlayed: 0,
          gamesWon: 0,
          gamesLost: 0,
          gamesTied: 0
        }
      }))();

      this.players = {
        human: new Player({name: 'human', mark: 'O'}),
        computer: new Player({name: 'computer', mark: 'X'})
      };

      this.layout = new MainLayout({
        state: this.state,
        players: this.players,
        stats: this.stats
      });

      // Grab a reference to the game view
      this.game = this.layout.game;

      // Track the current turn
      this.state.set('move', 0);
      this.listenTo(this.state, 'change:move', this.handleMove);

      // Listen to the state change and route accordingly
      this.listenTo(this.state, 'change:name', this.onStateChange);

      // Listen to a player change and start a new turn
      this.listenTo(this.state, 'change:player', this.startTurn);

      // Listen to a cell owner change and do calculations/game flow
      this.listenTo(this.layout.game, 'change:owner', this.handleChangeOwner);

      // Someone won!
      this.listenTo(this.state, 'change:winner', this.handleWinner);
    },

    // ##run
    // Start the application by showing the game view
    run: function() {
      console.log('running');
      this.layoutManager.showView(this.layout, {
        afterShow: _.bind(function() {
          this.state.set('name', 't3:started');
        }, this)
      });
    },

    handleWinner: function() {
      this.state.set('name', 't3:winner');
    },

    // ##handleChangeOwner
    // Run after a cell has been claimed
    handleChangeOwner: function(model, player) {
      var index = model.collection.indexOf(model);
      player.updatePairs(index);
      player.taken[index] = true;

      // Indicate that a move has been made
      this.state.set('move', this.state.get('move') + 1);
    },

    // ##handleMove
    // Run after a move has been recorded
    handleMove: function() {
      // Just switch the current player record
      this.swapPlayers();
    },

    // ##swapPlayers
    swapPlayers: function() {
      var player = null;
      if (this.state.get('player') === this.players.human) {
        player = this.players.computer;
      } else {
        player = this.players.human;
      }
      this.state.set('player', player);
    },

    // ##startTurn
    // Starts the turn by setting the game state
    startTurn: function() {
      this.options.state.set('name', 't3:turn-start');
    },

    // ##onChangeState:
    // When the state changes, route accordingly.
    onChangeState: function(model, state) {
      switch(state) {
        case 't3:started':
          // Kick start the game by setting the current player to 'human'
          this.state.set('player', this.players.human);
          break;

        case 't3:turn-start':
          var winningCells = this.game.findWinningCells();
          if (winningCells.length) {

            // Check for win condition
            var winner = winningCells[0].get('owner');
            this.state.set('winner', winner);
          } else if (this.state.get('move') >= 9) {

            // Otherwise, check for a tie game
            this.state.set('name', 't3:tie-game');
          }

          // Nothing is stopping the game from continuing...
          // Route to the correct turn state
          var player = this.state.get('player');
          this.state.set('name', 't3:' + player.get('name'));
          break;

        case 't3:computer':
          this.makeMove();
          break;

        case 't3:human':
          break;

        case 't3:winner':
//          var winner = this.state.get('winner');
          this.gameOver = new GameOver();
          $('.game', this.el).append(this.gameOver.render().el);
          break;

        case 't3:tie-game':
          this.gameOver = new GameOver();
          $('.game', this.el).append(this.gameOver.render().el);
      }
    },

    // ##makeMove
    // Run the computer move algorithm.
    //
    // 1) If there is a win, take it.
    // 2) Block the human's win
    // 3) Block the human's potential fork
    // 4) Play the center cell
    // 5) Play the opposite corner of the human
    // 6) Play an empty corner
    // 7) Play an empty side
    //
    // @see: http://stackoverflow.com/questions/125557/what-algorithm-for-
    //              a-tic-tac-toe-game-can-i-use-to-determine-the-best-
    //              move-for
    //
    //       http://rowdy.msudenver.edu/~gordona/cs1050/progs/
    //              tictactoermccsc.pdf
    //
    makeMove: function() {
      // Only allow the computer to do this.
      if (this.state.get('player') !== this.players.computer) { return; }

      // 1) Find a winning move
      var winningCell = this.game.getWinFor(this.players.computer.pairs);
      if (winningCell) {
        winningCell.set('owner', this.players.computer);
        console.log('found winning cell');
        return;
      }

      // 2) Block a human win
      var humanWin = this.game.getWinFor(this.players.human.pairs);
      if (humanWin) {
        humanWin.set('owner', this.players.computer);
        console.log('blocking a human win');
        return;
      }

      // 3) Block a potential human fork
      var forkCell = this.game.findForkFor(this.players.human);
      if (forkCell) {
        // A potential fork was found. To block it, assume that the forkCell
        // has been taken by the human and then re-run this algorithm to find a
        // cell that blocks the win.
        var blocker = this.game.findBlockForFork(forkCell, this.players.human);
        blocker.set('owner', this.players.computer);
        console.log('blocking a fork');
        return;
      }

      // 4) Play the center cell
      var center = this.game.getBoard().at(5);
      if (_.isNull(center.get('owner'))) {
        center.set('owner', this.players.computer);
        console.log('playing the center');
        return;
      }

      // 5) Play a corner opposite the human
      var opposite = this.game.getCornerOpposite(this.players.human);
      if (opposite) {
        opposite.set('owner', this.players.computer);
        console.log('playing the opposite corner');
        return;
      }

      // 6) Play an empty corner
      var emptyCorner = this.game.getEmptyCorner();
      if (emptyCorner) {
        emptyCorner.set('owner', this.players.computer);
        console.log('playing the empty corner');
        return;
      }

      // 7) Play an empty side
      var emptySide = this.game.getEmptySide();
      if (emptySide) {
        emptySide.set('owner', this.players.computer);
        console.log('playing the empty side');
        return;
      }
    },

    close: function() {
      // Close everything down
      this.trigger('close', this);
    }
  });

  return T3App;
});

