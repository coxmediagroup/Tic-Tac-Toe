define(['jquery', 'underscore', 'backbone', 'view/player/player', 'view/player/pcplayer'],
    function($, _, Backbone, BasePlayerView, PCPlayerView) {
        return Backbone.View.extend({
            tagName: 'section',
            id: 'gameState',

            initialize: function() {
                this.computerView = new BasePlayerView({
                    model: this.model.get('computer')
                });
                this.playerView = new PCPlayerView({
                    model: this.model.get('player')
                });
        },

        render: function() {
            this.$el.append(this.playerView.render().$el);
            this.$el.append(this.computerView.render().$el);

            return this;
        }
    });
});