define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.Model.extend({
        defaults: {
            isCurrent: false,
            playerName: 'Computer',
            playerType: 'NPC'
        },

        simulate: function(gameState) {
            var boardState = gameState.get('boardState');
            if (boardState[0][2] === 0) {
                boardState[0][2] = gameState.get('computer').get('playerType');
                gameState.unset('boardState', { silent : true });
                gameState.set('boardState', boardState);
            }
        }
    });
});