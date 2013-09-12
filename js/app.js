requirejs.config({
    baseUrl: 'js/libs', //load stuff from libs by default
    paths: {
        model: '../app/model', //setup model path
        view: '../app/view', //setup view path,
        controller: '../app/controller',
        backbone: 'backbone',
        underscore: 'underscore',
        jquery: 'jquery-2.0.3'
    },
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        }
    }
});

requirejs(['jquery', 'underscore', 'backbone', 'controller/applicationcontroller'],
    function($, _, Backbone, App) {
        var app = new App;
        app.run();
    }
);