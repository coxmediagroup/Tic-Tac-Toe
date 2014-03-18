/* global define */
define([
  'underscore',
  'backbone',
  'app-base',
  'apps',
  'layout-manager',
  'views'
], function(_, Backbone, AppBase, Apps, LayoutManager, Views) {
  'use strict';

  var Application = AppBase.extend({
    initialize: function() {
      // The layout manager controls the `Layout` view for this application.
      this.layoutManager = new LayoutManager({anchor: '#content'});

      // Monitors the state of the application
      this.state = new (Backbone.Model.extend({
        defaults: {
          name: 'app:stopped',
          player: null
        }
      }))();

      this.listenTo(this.state, 'change:name', this.onChangeState);
    },

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
          // Just as a note about how this could work:
          //
          // The idea is that each of these init methods ('chess:init', etc)
          // would initialize a sub application. I haven't implemented any of
          // them except for the 't3' application. However, they would all get
          // started similarly.
          //
          // Once a sub application starts, the State model would have new
          // state routes available to it. For example, the 't3:started' route
          // is only available when the t3 application has been initialized.
          //
          // The sub application would run itself (communicating back to the
          // parent only via State model changes). Eventually, the sub
          // application would stop running by issuing the 'exit' route (see
          // 't3:exit').

          $('.alert').html('Chess has not been installed').show().attr('title', '');
          break;

        // Initialize global thermonuclear war
        case 'gtnw:init':
          $('.alert').html('Global Thermalnuclear War is not currently available.' +
                           ' Please check back once Russia is scary again.').show();
          $('.alert').attr('title', 'Oh wait, I forgot about China');
          break;

        // Initialize tic-tac-toe
        case 't3:init':

          // If there's a current view, close it.
          var view = this.layoutManager.currentView;
          view.close();

          // The TicTacToe application shares the main app's layoutManager and
          // state.
          this.t3 && this.t3.close();
          this.t3 = new Apps.TicTacToe.App({
            layoutManager: this.layoutManager,
            state: this.state
          });
          this.t3.run();
          break;

        case 't3:exit':
          this.t3 && this.t3.close();
          this.state.set('name', 'app:started');
          break;

        default:
          // do nothing (someone else may handle it)
          break;
      }
    }
  });

  return Application;
});

