define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.Model.extend({
        isCurrent: false,
        playerName: undefined,
        playerType: undefined
    });
});