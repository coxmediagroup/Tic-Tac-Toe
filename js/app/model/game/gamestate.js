define(['jquery', 'underscore', 'backbone', 'model/player/player', 'model/player/npcplayer'],
    function($, _, Backbone, Player, NPCPlayer) {
     return Backbone.Model.extend({

         initialize: function() {
            this.set('player', new Player({
                playerType: 'PC',
                isCurrent: true
            }));
            this.set('computer', new NPCPlayer);
            this.set('currentPlayer', this.get('player'));
            this.set('boardState',  [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]);
         },

         sync: function(method, model, options) {

         }
     });
});