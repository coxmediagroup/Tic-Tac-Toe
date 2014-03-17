/* global define */
define([
  'underscore',
  'backbone-layout',
  'layout-manager'
], function(_, Layout, LayoutManager) {
  'use strict';

  var Header = Layout.extend({
    className: 'game-header'
  });

  var Footer = Layout.extend({
    className: 'game-footer'
  });

  var StartupView = Layout.extend({
    className: 'game-startup'
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
      options || (options = {});

      // Create a manager for the actual game view (i.e. the area where views
      // may swap in/out)
      this.layoutManager = new LayoutManager({
        anchor: '.game-view',
        context: this.$el
      });

      // Register sub views (see `backbone-layout`)
      this.header = new Header();
      this.footer = new Footer();
      this.registerView(this.header, {anchor: '.game-header', replace: true});
      this.registerView(this.footer, {anchor: '.game-footer', replace: true});

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
          this.layoutManager.showView(new StartupView());
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
