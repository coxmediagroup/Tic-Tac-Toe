define(['jquery', 'underscore', 'backbone', 'view/player/player'], function($, _, Backbone, PlayerView) {
    return Backbone.View.extend({
        tagName: 'div',
        className: 'container',

        initialize: function() {
            this.computerView = new PlayerView({
                model: this.model.get('computer')
            });
            this.playerView = new PlayerView({
                model: this.model.get('player')
            });
        },

        render: function() {
            this.$el.append(this.playerView.render().el);
            this.$el.append(this.computerView.render().el);

            return this;
        }
    });
});