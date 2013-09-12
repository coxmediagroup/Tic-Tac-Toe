define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.Model.extend({
        defaults: {
            isCurrent: false,
            playerName: undefined,
            playerType: undefined
        }
    });
});