define(['backbone', 'view/game/game', 'model/game/gamestate'],
    function(Backbone, GameView, GameState){
        return Backbone.Router.extend({
            routes : {
                '': 'newGame',
                'new': 'newGame',
                'continue': 'continueGame',
                'quit': 'quitGame'
            },

            initialize: function() {
                this.gameState = new GameState;
                this.gameView = new GameView({ model: this.gameState });
            },

            run: function() {
                Backbone.history.start({
                    pushState: true,
                    root : 'C:/Users/ev0v2vn/tests/Tic-Tac-Toe/index.html'
                });
            },

            newGame: function() {
                this.gameState.destroy();
                this.continueGame();
            },

            continueGame: function() {
                this.gameState.fetch();
                this.gameView.render();
            },

            quitGame: function() {
                this.gameState.save();
                this.gameView.render();
            }
        })
    }
);