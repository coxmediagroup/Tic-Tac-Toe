define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.Model.extend({
        defaults: {
            boardMatrix: [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        }
    });
});