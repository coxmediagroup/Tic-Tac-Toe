define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.View.extend({
        tagName: 'div',
        id: 'board',

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        }
    });
});