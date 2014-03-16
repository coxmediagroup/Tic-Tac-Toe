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
      defaults: {name: 'stopped'}
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
            this.state.set('name', 't3:started');
          }, this));

          // Now show the view.
          this.layoutManager.showView(titleScreen);
          break;

        // The tic-tac-toe game has been started
        case 't3:started':
          var t3game = new Views.T3();
          this.layoutManager.showView(t3game);
          break;

        default:
          throw new Error('no available state handler for ' + state);
      }
    }
  });

  return Application;
});

