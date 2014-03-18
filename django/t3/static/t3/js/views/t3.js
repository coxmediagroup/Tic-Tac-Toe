/* global define */
define([
  'underscore',
  'backbone',
  'backbone-layout'
], function(_, Backbone, Layout) {
  'use strict';

  var Header = Layout.extend({
    className: 'game-header',

    template: _.template(
      '<div class="header">' +
      '  <div class="games-played">' +
      '    <label>Played:</label>' +
      '    <span class="value"><%= gamesPlayed %></span>' +
      '  </div>' +
      '  <div class="games-won">' +
      '    <label>Won:</label>' +
      '    <span class="value"><%= gamesWon %></span>' +
      '  </div>' +
      '  <div class="games-lost">' +
      '    <label>Lost:</label>' +
      '    <span class="value"><%= gamesLost %></span>' +
      '  </div>' +
      '  <div class="games-tied">' +
      '    <label>Tied:</label>' +
      '    <span class="value"><%= gamesTied %></span>' +
      '  </div>' +
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      this.listenTo(this.model, 'change', this.render);
    }
  });

  var Footer = Layout.extend({
    className: 'game-footer',

    template: _.template(
      '<div class="footer">' +
      '  <div class="game-player">' +
      '    <label>Player:</label>' +
      '    <span class="value"><%= player %></span>' +
      '  </div>' +
      '  <div class="game-move">' +
      '    <label>Move:</label>' +
      '    <span class="value"><%= move %></span>' +
      '  </div>' +
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      this.listenTo(this.model, 'change:player', this.render);
      this.listenTo(this.model, 'change:move', this.render);
    },

    serialize: function() {
      return {
        player: this.model.get('player').get('name'),
        move: this.model.get('move')
      };
    }
  });

  // To make checking for wins a little faster, just store the valid winning
  // cell combinations as a constant.
  var WINNING_COMBOS = [
    // Rows       Cols      Diags
    [8, 1, 6], [8, 3, 4], [8, 5, 2],
    [3, 5, 7], [1, 5, 9], [6, 5, 4],
    [4, 9, 2], [6, 7, 2]
  ];

  var Board = Backbone.Collection.extend({

    // Returns the cells that could win the game for the player
    findWins: function(pairs) {
      var wins = this.filter(function(cell, index) {
        if (index === 0) { return; }
        if (!cell.get('owner')) {
          if (pairs[15 - index]) {
            return cell;
          }
        }
      });

      return wins;
    },

    deepClone: function() {
      return new this.constructor(this.models.map(function(m) {
        return m.clone();
      }));
    },

    isCenterOpen: function() {
      return _.isNull(this.at(5).get('owner'));
    },

    findOppositeCorners: function(player) {
      var ownedCorners = this.filter(function(cell, index) {
        if (index === 0) { return false; }

        // All the corner cells are evens
        var isCorner = !(function() {
          return index % 2;
        })();

        return isCorner && cell.get('owner') === player;
      });

      return _.filter(ownedCorners, function(corner) {
        var cornerIdx = this.indexOf(corner);

        // The opposite corners always add up to 10
        return _.isNull(this.at(10 - cornerIdx).get('owner'));
      }, this);
    },

    findEmptyCorners: function() {
      return this.filter(function(cell, index) {
        if (index === 0) { return false; }
        var isCorner = !(function() {
          return index % 2;
        })();
        return isCorner && _.isNull(cell.get('owner'));
      });
    },

    findEmptySides: function() {
      return this.filter(function(cell, index) {
        if (index === 0) { return false; }
        var isSide = (function() { return index % 2; })();
        return isSide && _.isNull(cell.get('owner'));
      });
    },

    findWinningCells: function() {
      _.each(WINNING_COMBOS, function(cellIds) {
        var cells = _.map(cellIds, function(num) {
          return this.at(num);
        }, this);
        var byPlayer = _.countBy(cells, function(cell) {
          return cell.player.get('name');
        });
        if (byPlayer.computer === 3) {
          return cells;
        } else if (byPlayer.human === 3) {
          return cells;
        }
      }, this);

      return [];
    }
  });

  var Game = Layout.extend({
    className: 'game-view',

    template: _.template(
      '<div class="game">' +
        '<div class="t3-row row-1">' +
        '  <div data-val="8" class="t3-col col-1"><%= mark[8] %></div>' +
        '  <div data-val="1" class="t3-col col-2"><%= mark[1] %></div>' +
        '  <div data-val="6" class="t3-col col-3"><%= mark[6] %></div>' +
        '</div>' +
        '<div class="t3-row row-2">' +
        '  <div data-val="3" class="t3-col col-1"><%= mark[3] %></div>' +
        '  <div data-val="5" class="t3-col col-2"><%= mark[5] %></div>' +
        '  <div data-val="7" class="t3-col col-3"><%= mark[7] %></div>' +
        '</div>' +
        '<div class="t3-row row-3">' +
        '  <div data-val="4" class="t3-col col-1"><%= mark[4] %></div>' +
        '  <div data-val="9" class="t3-col col-2"><%= mark[9] %></div>' +
        '  <div data-val="2" class="t3-col col-3"><%= mark[2] %></div>' +
        '</div>' +
      '</div>'
    ),

    events: {
      'click .t3-col': 'handleClick'
    },

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);

      this.board = new Board([
        { owner: null }, // ignore index 0
        { owner: null }, { owner: null }, { owner: null },
        { owner: null }, { owner: null }, { owner: null },
        { owner: null }, { owner: null }, { owner: null }
      ]);

      this.computer = new Player({name: 'computer', mark: 'X'});
      this.human = new Player({name: 'human', mark: 'O'});
      this.options.state.set('player', this.human);

      this.listenTo(this.board, 'change:owner', this.handleChangeOwner);

      // Track the number of moves
      this.options.state.set('move', 0);
      this.listenTo(this.options.state, 'change:move', this.handleMove);
    },

    serialize: function() {
      return {
        mark: this.board.map(function(cell) {
          if (!cell.get('owner')) {
            return '';
          } else {
            return cell.get('owner').get('mark');
          }
        })
      };
    },

    handleMove: function() {
      this.swapPlayer();
    },

    handleChangeOwner: function(model, player) {
      var cellId = model.collection.indexOf(model);

      // Update the player's pairs
      player.updatePairs(cellId);

      // Mark this cell as taken
      player.taken[cellId] = true;

      this.render();

      // Increment the move counter
      this.options.state.set('move', this.options.state.get('move') + 1);
    },

    handleClick: function(event) {
      var cellId = Number($(event.target).data('val'));
      var player = this.options.state.get('player');

      // Update the owner
      this.board.at(cellId).set('owner', player);
    },

    swapPlayer: function() {
      if (this.options.state.get('player') === this.human) {
        this.options.state.set('player', this.computer);
      } else {
        this.options.state.set('player', this.human);
      }
    },

    calculateMove: function() {
      // Only the computer should do this
      if (this.options.state.get('player') !== this.computer) {
        return;
      }

      var winningCells = this.board.findWins(this.computer.pairs);
      if (winningCells.length) {
        // A winning cell was found, take it!
        winningCells[0].set('owner', this.computer);
        console.log('detected winning cell', winningCells[0]);
      } else {
        // No winning cell was found. Now the alternatives have to be
        // considered

        // First, check if there is a cell that blocks the human player from
        // winning
        // If things went correctly, the results should never be more than 1
        var humanWins = this.board.findWins(this.human.pairs);

        if (humanWins.length) {
          // This cell would win for the human, block it.
          humanWins[0].set('owner', this.computer);
          console.log('detected winning human cell', humanWins);
        } else {

          // No cell was found to block the human from winning. Now, check if
          // there is a place the human can fork next turn
          var human = this.human;
          var forkBlocks = this.board.filter(function(cell, index) {
            var clone = human.deepClone();

            // Ignore 0 index and any owned cells
            if (index === 0 || cell.get('owner')) { return false; }

            // Check if, after this cell has been taken, the human has a
            // winning move.
            clone.taken[index] = true;
            clone.updatePairs(index);
            var humanWins = this.findWins(clone.pairs);

            // If there is just one win then it's safe to just ignore it
            // because the algorithm already knows how to block a single
            // winning move.
            if (humanWins.length === 2) {

              // If there are two wins, this is a potential fork. Return the
              // index so we can access the correct cell.
              return index;
            }

            // This cell doesn't block a fork.
            return false;
          }, this.board);

          // Again, if things went right the forkBlocks should only ever
          // contain at most one element.
          if (forkBlocks.length) {

            // A potential fork was found, block it!
            forkBlocks[0].set('owner', this.computer);
            console.log('detected potential fork', this.board.at(forkBlocks[0]));
          } else if (this.board.isCenterOpen()) {

            // If the center cell is open, take it.
            this.board.at(5).set('owner', this.computer);
            console.log('taking the center', this.board.at(5));
          } else {

            // Find the corners opposite the ones the human has claimed
            var corners = this.board.findOppositeCorners(this.human);
            if (corners.length) {

              // A corner is open that is opposite the human player, take it.
              corners[0].set('owner', this.computer);
              console.log('taking the opposite corner', corners[0]);
            } else {

              // Find an empty corner
              var emptyCorner = this.board.findEmptyCorners();
              if (emptyCorner.length) {
                emptyCorner[0].set('owner', this.computer);
                console.log('taking an empty corner', emptyCorner[0]);
              } else {

                // Find an empty side
                var emptySide = this.board.findEmptySides();
                if (emptySide.length) {
                  emptySide[0].set('owner', this.computer);
                  console.log('taking an empty side', emptySide[0]);
                }
              }
            }
          }
        }
      }
    }
  });

  // TicTacToe
  // ---------

  // The `Tic-Tac-Toe` game view is really more of an applicaiton. It is in
  // charge of application state management that relate to the 't3'
  // application.
  //
  // If I were to spend more time on this I'd probably make this an actual
  // `Application` sub class and make sure that every time it changes
  // application state, that the name of that state would be prepended with
  // 't3:', but that would probably take a little longer to implement than is
  // really required.
  var TicTacToe = Layout.extend({
    className: 't3-game',

    template: _.template(
      '<div class="game-header"></div>' +
      '<div class="game-view"></div>' +
      '<div class="game-footer"></div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      options || (options = {});

      // Keep some basic game stats
      this.stats = new (Backbone.Model.extend({
        defaults: {
          gamesPlayed: 0,
          gamesWon: 0,
          gamesLost: 0,
          gamesTied: 0
        }
      }))();

      // Registered views will automatically be rendered when their parent is
      // rendered. (see `backbone-layout`)
      this.header = new Header({model: this.stats});
      this.footer = new Footer({model: this.options.state});
      this.game = new Game({state: this.options.state});
      this.registerView(this.header, {anchor: '.game-header', replace: true});
      this.registerView(this.footer, {anchor: '.game-footer', replace: true});
      this.registerView(this.game, {anchor: '.game-view', replace: true});

      // Listen to the state model's state changes.
      this.listenTo(this.options.state, 'change:name', this.onChangeState);
      this.listenTo(this.options.state, 'change:player', function() {
        this.options.state.set('name', 't3:turn-start');
      }, this);
    },

    afterRender: function() {
      this.options.state.set('name', 't3:started');
    },

    checkWin: function() {
      return this.game.board.findWinningCells();
    },

    // Handle state changes that relate to the t3 game.
    onChangeState: function(model, state) {
      switch(state) {
        case 't3:started':
          break;

        case 't3:turn-start':
          // Check for win conditions, etc
          var winningCells = this.checkWin();
          if (winningCells) {
            this.game.highlight(winningCells);
            var winner = winningCells[0].get('owner');
            this.options.state.set('name', 't3:winner-' + winner.get('name'));
          }

          var player = this.options.state.get('player');
          this.options.state.set('name', 't3:' + player.get('name'));
          break;

        case 't3:computer':
          this.game.calculateMove();
          break;

        case 't3:human':
          break;

        case 't3:winner-computer':
          break;

        case 't3:winner-human':
          break;

        default:
          break;
      }
    }
  });

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

  return TicTacToe;
});

