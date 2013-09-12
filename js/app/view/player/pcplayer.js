define(['jquery', 'underscore', 'backbone', 'view/player/player'], function($, _, Backbone, PlayerView) {
    return PlayerView.extend({
        events: {
            'blur .input': "inputChange",
            'keypress .input': "inputKeyPress"
        },

        template: function(model) {
            var renderedHtml = this.templateHtml;

            if (this.model.get('playerName') === undefined) {
                renderedHtml = '<div class="input-container"><label for="playerName">Player Name</label>';
                renderedHtml += '<input class="input" type="textbox" id="playerName"/></div>';
            }

            return _.template(renderedHtml, {
                playerName: model.get('playerName'),
                playerType: model.get('playerType')
            });
        },

        inputChange: function(event) {
            var val = $(event.currentTarget).val();
            if (val !== '') this.model.set('playerName', val);
        },

        inputKeyPress: function(event) {
            var code = event.keyCode || event.which;
            if (code === 13) {
                this.inputChange(event);
            }
        }
    });
});