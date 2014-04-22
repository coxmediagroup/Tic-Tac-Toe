
// contents of main.js:
require.config({
    'paths': {
        'backbone': 'backbone/1.0.0/backbone-min',
        'bootstrap': 'bootstrap/3.1.1/bootstrap.min',
        'jquery': 'jquery/1.11.0/jquery-1.11.0.min',
        'knockback': 'knockback/0.18.4/knockback',
        'knockout': 'knockout/2.2.0/knockout-2.2.0',
        'underscore': 'underscore/1.5.0/underscore-min'
    },
    'shim': {
        'bootstrap' : ['jquery'],
    }
});

// Load the main app module to start the app
require(['tictac'], function(tictac) {
  return tictac.didLaunch();
});

