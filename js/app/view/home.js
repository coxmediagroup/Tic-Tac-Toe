define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.View.extend({
        tagName: 'div',
        className: 'homecontainer',
        events: {
            'keypress #playerName' : 'onKeyPress',
            'blur #playerName': 'onInputChange'
        },

        templateHtml: '<label for="playerName">Player Name</label><input type="textbox" id="playerName" />',

        initialize: function() {
            this.listenTo(this.model, "change", this.gameUpdate);
        },

        onKeyPress: function(event) {
            if (event.which === 13) {
                this.onInputChange(event);
            }
        },

        onInputChange: function(event) {
            var name = $(event.target).val();
            this.model.set('playerName', name);
        },

        template: function() {
            var html = '<h1>Shall we play a game? ... How about Global Thermonuclear War.</h1>';
            html += _.template(this.templateHtml);
            return html;
        },

        gameUpdate: function() {
            this.trigger('game:new');
        },

        render: function() {
            this.$el.html(this.template());
            $('body').html(this.$el);
            return this;
        }
    });
});