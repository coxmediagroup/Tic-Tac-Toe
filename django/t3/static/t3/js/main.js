require.config({
  paths: {
    'jquery': '../components/jquery/dist/jquery',
    'backbone': '../components/backbone/backbone',
    'underscore': '../components/underscore/underscore',
    'backbone-layout': '../components/backbone-layout/backbone-layout',
    'bootstrap': '../components/bootstrap/dist/js/bootstrap'
  },
  shim: {
    'jquery': {
      exports: '$'
    },
    'underscore': {
      exports: '_'
    },
    'backbone': {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    'bootstrap': {
      deps: ['jquery']
    },
    'backbone-layout': {
      deps: ['backbone']
    }
  }
});

/* global define */
define(['application', 'bootstrap'], function(Application) {
  'use strict';

  var app = new Application({ debug: true });

  // Monitor the status of the application
  app.on('application:run', function() {
    console && (console.log('running', arguments));
  });
  app.on('application:close', function() {
    console && (console.log('closed', arguments));
  });

  app.run();
});
