define(['jquery', 'underscore', 'backbone', 'model/player/player', 'model/game/boardstate'],
    function($, _, Backbone, Player, BoardState) {
     return Backbone.Model.extend({
         initialize: function() {
            this.set('player', new Player({
                playerType: 'PC'
            }));
            this.set('computer', new Player({
                isCurrent: true,
                playerName: 'Computer',
                playerType: 'NPC'
            }));
            this.set('currentPlayer', this.get('computer'));
            this.set('boardState', new BoardState);
         },

         sync: function(method, model, options) {

         }
     });
});