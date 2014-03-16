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
  };

  // Extend Application with inheritable properties.
  _.extend(Application.prototype, Backbone.Events, {

    // Run the application
    run: function() {
      this.trigger('application:run', this);

      // Show the title screen once the application starts up.
      this.layoutManager.showView(new Views.TitleScreen());
    },

    // Close the application
    close: function() {
      this.trigger('application:close', this);
    },

    // Handle application state changes
    onChangeState: function() {
    }
  });

  return Application;
});

