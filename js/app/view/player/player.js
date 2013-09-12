define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.View.extend({
        tagName: 'div',
        className: 'player',

        templateHtml: '<div class="field" id="<%= playerType %>"><%= playerName %></div>',

        initialize: function() {
            this.listenTo(this.model, "change", this.render);
        },

        template: function(model) {
            return _.template(this.templateHtml, {
                playerName: model.get('playerName'),
                playerType: model.get('playerType')
            });
        },

        render: function() {
            this.$el.toggleClass('current', this.model.get('isCurrent'));
            this.$el.html(this.template(this.model));
            return this;
        }
    });
});