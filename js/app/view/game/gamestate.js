define(['jquery', 'underscore', 'backbone', 'view/player/player'],
    function($, _, Backbone, PlayerView) {
        return Backbone.View.extend({
            tagName: 'section',
            id: 'gameState',
            events : {
                'click #restart': 'onRestartClick'
            },

            initialize: function() {
                this.computerView = new PlayerView({
                    model: this.model.get('computer')
                });
                this.playerView = new PlayerView({
                    model: this.model.get('player')
                });
            },

            render: function() {
                this.$el.append(this.playerView.render().$el);
                this.$el.append(this.computerView.render().$el);

                if (this.model.isGameOver()) {
                    this.$el.append('<button id="restart">Restart Game</button>');
                }

                return this;
            },

            onRestartClick: function() {
                this.model.trigger('game:restart');
            }
    });
});