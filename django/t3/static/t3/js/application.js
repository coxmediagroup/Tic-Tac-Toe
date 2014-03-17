/* global define */
define([
  'underscore',
  'backbone',
  'layout-manager',
  'views'
], function(_, Backbone, LayoutManager, Views) {
  'use strict';

  var Application = function() {
    // The layout manager controls the `Layout` view for this application.
    this.layoutManager = new LayoutManager({anchor: '#content'});

    // Monitors the state of the application
    this.state = new (Backbone.Model.extend({
      defaults: {name: 'app:stopped'}
    }))();

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
            this.state.set('name', 't3:init');
          }, this));

          // Now show the view.
          this.layoutManager.showView(titleScreen);
          break;

        // The tic-tac-toe game initialization
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

