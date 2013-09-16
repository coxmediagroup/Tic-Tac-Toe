define(['backbone', 'view/game/game', 'view/home', 'model/game/gamestate'],
    function(Backbone, GameView, HomeView, GameState){
        return Backbone.Router.extend({
            routes : {
                '': 'home',
                'new': 'newGame',
                'continue': 'continueGame',
                'quit': 'quitGame'
            },

            initialize: function() {
                this.gameState = new GameState;
                this.gameView = new GameView({ model: this.gameState });
                this.listenTo(this.gameState, 'change', this.onGameUpdate);
            },

            run: function() {
                Backbone.history.start({
                    pushState: true,
                    root : 'C:/Users/ev0v2vn/tests/Tic-Tac-Toe/index.html'
                });
            },

            home: function() {
                this.homeView = new HomeView({ model : this.gameState.get('player') });
                this.listenTo(this.homeView, 'game:new', this.newGame);
                this.homeView.render();
            },

            newGame: function() {
                this.gameState.destroy();
                this.homeView.remove();
                this.gameView.render();
            },

            continueGame: function() {
                this.gameState.fetch();
                this.gameView.render();
            },

            quitGame: function() {
                this.gameState.save();
                this.gameView.render();
            },

            onGameUpdate: function() {     //comes from a view update made by a user.
                var computer = this.gameState.get('computer');
                var player = this.gameState.get('player');

                this.updateGameState();  //update the game state.

                if (computer.get('isCurrent') && !this.gameState.isGameOver()) {  //if we're now the computer
                    computer.simulate(this.gameState);
                }
            },

            updateGameState: function() {
                var currentPlayer = this.gameState.get('currentPlayer');

                if (!this.gameState.isGameOver()) {
                    if (currentPlayer.get('playerType') === 'NPC') {
                        this.gameState.set('currentPlayer', this.gameState.get('player'), { silent: true });
                        this.gameState.get('player').set('isCurrent', true);
                        this.gameState.get('computer').set('isCurrent', false);
                    } else {
                        this.gameState.set('currentPlayer', this.gameState.get('computer'), { silent: true });
                        this.gameState.get('player').set('isCurrent', false);
                        this.gameState.get('computer').set('isCurrent', true);
                    }
                } else {
                    this.stopListening(this.gameState, 'change', this.onGameUpdate);
                    this.gameState.get('currentPlayer').set('isWinner', true);
                    if (this.gameState.allMovesMade() && !this.gameHasWinner()) {
                        var type = this.gameState.get('currentPlayer').get('playerType');

                        if (type === 'NPC') {
                            this.gameState.get('player').set('isWinner', true);
                        } else {
                            this.gameState.get('computer').set('isWinner', true);
                        }
                    }
                }
            }
        })
    }
);