define(['jquery', 'underscore', 'backbone', 'model/player/player'], function($, _, Backbone, Player) {
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
            this.set('boardState', [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
             ]);
         },

         sync: function(method, model, options) {

         }
     });
});