/* global define */
define([
  'underscore',
  'backbone',
  'layout-manager',
  'views'
], function(_, Backbone, LayoutManager, Views) {
  'use strict';

  var Application = function(options) {
    // The layout manager controls the `Layout` view for this application.
    this.layoutManager = new LayoutManager({anchor: '#content'});

    // Monitors the state of the application
    this.state = new (Backbone.Model.extend({
      defaults: {
        name: 'app:stopped',
        player: null
      },

      swapPlayer: function() {
        if (this.get('player') === 'human') {
          this.set('player', 'computer');
        } else {
          this.set('player', 'human');
        }
      }
    }))();

    options || (options = {});
    this.options = options;

    this.listenTo(this.state, 'change:name', this.onChangeState);
  };

  // Extend Application with inheritable properties.
  _.extend(Application.prototype, Backbone.Events, {

    // Run the application
    run: function() {
      this.trigger('application:run', this);
      this.state.set('name', 'app:started');
    },

    // Close the application
    close: function() {
      this.trigger('application:close', this);
    },

    // Handle application state changes.
    onChangeState: function(model, state) {
      switch(state) {

        // The application has started, the game isn't running yet.
        case 'app:started':

          // Create the title screen view and handle click events
          var titleScreen = new Views.TitleScreen();
          titleScreen.on('click:yes', _.bind(function() {
            this.state.set('name', 'app:choose');
          }, this));

          // Now show the view.
          this.layoutManager.showView(titleScreen);
          this.options.debug && this.state.set('name', 'app:choose');
          break;

        // Choose what game to play (better not try global thermonuclear war!)
        case 'app:choose':
          var choose = new Views.Choose();
          choose.on('play', _.bind(function(name) {
            this.state.set('name', name + ':init');
          }, this));
          this.layoutManager.showView(choose);
          break;

        // Initialize chess
        case 'chess:init':
          break;

        // Initialize global thermonuclear war
        case 'gtnw:init':
          break;

        // Initialize tic-tac-toe
        case 't3:init':

          // Make sure previous games are closed (if any)
          this.game && this.game.close();

          // Start the game up. The T3 game needs to have access to the state
          // model (it's more of an application than a view anyway).
          this.game = new Views.T3({state: this.state});
          this.layoutManager.showView(this.game);
          break;

        default:
          // do nothing (someone else may handle it)
          break;
      }
    }
  });

  return Application;
});

