define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.View.extend({
        tagName: 'div',
        className: 'player',

        templateHtml: '<div id="<%= playerType %>"><%= playerName %></div>',

        template: function(model) {
            return _.template(this.templateHtml, {
                playerName: model.get('playerName'),
                playerType: model.get('playerType')
            });
        },

        render: function() {
            this.$el.html(this.template(this.model));

            return this;
        }
    });
});