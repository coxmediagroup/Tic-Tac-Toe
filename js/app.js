requirejs.config({
    baseUrl: 'js/libs', //load stuff from libs by default
    paths: {
        model: 'js/app/model', //setup model path
        view: 'js/app/view', //setup view path,
        controller: 'js/app/controller' //setup controller path
    },
    map: { //setup jquery to use noConflict
        '*': {
            'jquery': 'jquery-noconflict',
            'backbone': 'backbone-noconflict',
            'underscore': 'underscore-noconflict'
        },
        'backbone': { 'backbone': 'backbone'},
        'underscore': {'underscore': 'underscore'},
        'jquery-noconflict': { 'jquery': 'jquery-2.0.3' }
    }
});

requirejs(['jquery', 'underscore', 'backbone', 'controller/applicationcontroller'],
    function($, _, Backbone, AppController) {
        var application = new AppController;
        application.init();
    }
);