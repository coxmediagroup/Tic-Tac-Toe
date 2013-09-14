define(['jquery', 'underscore', 'backbone', 'view/game/gamestate', 'view/game/gameboard'],
    function($, _, Backbone, GameStateView, GameBoardView) {
        return Backbone.View.extend({
            tagName: 'div',
            className: 'wrapper',
            id: 'app',

            initialize : function(options) {
                this.gameStateView = new GameStateView({
                    model: options.model
                });
                this.gameBoardView = new GameBoardView({
                    model:  options.model
                });
            },

            render: function() {
                this.$el.append(this.gameStateView.render().$el).append(this.gameBoardView.render().$el);
                $('body').html(this.$el);

                return this;
            }
    });
});