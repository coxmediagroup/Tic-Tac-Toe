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
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      this.listenTo(this.model, 'change:player', this.render);
    }
  });

  var Game = Layout.extend({
    className: 'game-view',

    template: _.template(
      '<div class="game">' +
        '<div class="t3-row row-1">' +
        '  <div class="t3-col col-1"></div>' +
        '  <div class="t3-col col-2"></div>' +
        '  <div class="t3-col col-3"></div>' +
        '</div>' +
        '<div class="t3-row row-2">' +
        '  <div class="t3-col col-1"></div>' +
        '  <div class="t3-col col-2"></div>' +
        '  <div class="t3-col col-3"></div>' +
        '</div>' +
        '<div class="t3-row row-3">' +
        '  <div class="t3-col col-1"></div>' +
        '  <div class="t3-col col-2"></div>' +
        '  <div class="t3-col col-3"></div>' +
        '</div>' +
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);

      this.rows = [
        new Cells([{mark: null}, {mark: null}, {mark: null}]),
        new Cells([{mark: null}, {mark: null}, {mark: null}]),
        new Cells([{mark: null}, {mark: null}, {mark: null}])
      ];

      _.each(this.rows, function(collection, index) {
        var i = index + 1;
        this.registerView(new Cell({
          model: collection.models[0],
          state: this.options.state
        }), {
          anchor: '.row-' + i + ' .col-1'
        });
        this.registerView(new Cell({
          model: collection.models[1],
          state: this.options.state
        }), {
          anchor: '.row-' + i + ' .col-2'
        });
        this.registerView(new Cell({
          model: collection.models[2],
          state: this.options.state
        }), {
          anchor: '.row-' + i + ' .col-3'
        });

        this.listenTo(collection, 'change:mark', function() {
          this.options.state.swapPlayer();
        }, this);
      }, this);
    }
  });

  var Cells = Backbone.Collection.extend();

  var Cell = Layout.extend({
    className: 'cell',

    events: {
      'click': 'onClick'
    },

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      this.listenTo(this.model, 'change:mark', function(model, value) {
        this.$el.html(value);
      });
    },

    getMark: function(player) {
      if (player === 'human') {
        return 'X';
      } else {
        return 'O';
      }
    },

    onClick: function() {
      this.model.set('mark', this.getMark(this.options.state.get('player')));
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

      // Listen to the game view for turn swaps
    },

    afterRender: function() {
      this.options.state.set('name', 't3:started');
    },

    // Handle state changes that relate to the t3 game.
    onChangeState: function(model, state) {
      switch(state) {
        case 't3:started':
          model.set('player', 'human');
          break;
        default:
          break;
      }
    }
  });

  return TicTacToe;
});

