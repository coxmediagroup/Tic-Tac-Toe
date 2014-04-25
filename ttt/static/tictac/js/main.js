
// contents of main.js:
require.config({
    paths: {
        'backbone': 'backbone/1.0.0/backbone-min',
        'bootstrap': 'bootstrap/3.1.1/bootstrap',
        'jquery': 'jquery/1.11.0/jquery-1.11.0.min',
        'knockback': 'knockback/0.18.4/knockback',
        'knockout': 'knockout/2.2.0/knockout-2.2.0',
        'underscore': 'underscore/1.5.0/underscore-min'
    },
    shim: {
        'jquery': {
            exports: 'jQuery',
        },
        'underscore': {
            deps: [],
            exports: '_'
        },
        'backbone': {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        'bootstrap': {
            deps: ['jquery'],
            exports: '$.fn.modal',
        }
    }
});

// Load the main app module to start the app
require(['tictac'], function(tictac) {
  return tictac.didLaunch();
});

