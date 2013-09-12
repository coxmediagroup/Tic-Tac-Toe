define(['backbone', 'view/GameView', 'model/GameState'],
    function(Backbone, GameView, GameState){
        return Backbone.Router.extend({
            routes : {
                '': 'newGame',
                'new': 'newGame',
                'continue': 'continueGame',
                'quit': 'quitGame'
            },

            initialize: function() {
                this.gameView = new GameView;
                this.gameState = new GameState;
            },

            run: function() {
                Backbone.history.start({pushState: true});
            },

            newGame: function() {
                this.gameState.delete();
                this.continueGame();
            },

            continueGame: function() {
                this.gameState.load();
                this.gameView.render();
            },

            quitGame: function() {
                this.gameState.delete();
                this.gameView.render();
            }
        })
    }
);