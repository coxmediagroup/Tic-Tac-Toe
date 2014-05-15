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

                this.listenTo(this.model, 'change', function(){
                    if (this.model.isGameOver()) {
                        this.stopListening(this.model, 'change');
                        this.$el.append('<button id="restart">Restart Game</button>');
                    }
                });
            },

            render: function() {
                this.$el.append(this.playerView.render().$el);
                this.$el.append(this.computerView.render().$el);
                return this;
            },

            onRestartClick: function() {
                this.model.trigger('game:restart');
            }
    });
});