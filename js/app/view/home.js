define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.View.extend({
        tagName: 'div',
        className: 'homecontainer',
        events: {
            'keypress #playerName' : 'onKeyPress',
            'blur #playerName': 'onInputChange'
        },

        templateHtml: '<input type="textbox" id="playerName">',

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
            if (name !== '') {
                this.model.set('playerName', name);
            }
        },

        template: function() {
            return _.template(this.templateHtml);
        },

        gameUpdate: function() {
            this.trigger('game:new');
        },

        render: function() {
            this.$el.append('<h3>Shall we play a game,' + this.templateHtml + '?</h3>');
            this.$el.append('<h3>How about Global Thermonuclear War.</h3>');
            $('body').html(this.$el);
            return this;
        }
    });
});