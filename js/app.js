requirejs.config({
    baseUrl: 'js/libs', //load stuff from libs by default
    paths: {
        model: '../app/model', //setup  js/app/model path
        view: '../app/view', //setup  js/app/view path,
        controller: '../app/controller', //setup js/app/controller path
        backbone: 'backbone',  //setup backbone
        underscore: 'underscore', //setup underscore
        jquery: 'jquery-2.0.3' //setup jquery
    },
    shim: {
        underscore: {
            exports: '_' //setup shim for underscore so it actually loads
        },
        backbone: {
            deps: ['jquery', 'underscore'],  //setup dependencies for backbone so it actually loads
            exports: 'Backbone'
        }
    }
});

requirejs(['controller/gamecontroller'],
    function(Game) {
        var game = new Game;
        game.run();
    }
);