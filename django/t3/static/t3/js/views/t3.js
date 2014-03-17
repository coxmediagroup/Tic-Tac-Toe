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
    className: 'game-footer'
  });

  var Game = Layout.extend({
    className: 'game-view',

    template: _.template(
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
      '</div>'
    )
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
      this.footer = new Footer();
      this.game = new Game();
      this.registerView(this.header, {anchor: '.game-header', replace: true});
      this.registerView(this.footer, {anchor: '.game-footer', replace: true});
      this.registerView(this.game, {anchor: '.game-view', replace: true});

      // Listen to the state model's state changes.
      this.listenTo(this.options.state, 'change:name', this.onChangeState);
    },

    afterRender: function() {
      this.options.state.set('name', 't3:start');
    },

    // Handle state changes that relate to the t3 game.
    onChangeState: function(model, state) {
      switch(state) {
        case 't3:start':
          this.options.state.set('name', 'started');
          break;
        case 't3:started':
          break;
        default:
          break;
      }
    }
  });

  return TicTacToe;
});

