var Square = Backbone.Model.extend({
    defaults: {
        isX: undefined,
        warning: undefined
    },

    playerMove: function() {
        switch (this.attributes.isX) {
            case undefined:
                this.set({isX: true});
                break;
            case true:
                this.set({warning: "you've already selected this square"});
                break;
            default:
                this.set({warning: "this square has already been chosen"});
                break;
        }
    },

    isOpen: function() {
        return this.attributes.isX === undefined;
    }
});

var SquareView = Backbone.View.extend({
    tagName: "div",
    className: "square",
    events: {
        "click": "squareClick"
    },
    template: _.template("<% if (warning) { %><%= warning %><% } else { %><span><% if (isX === undefined) { %><% } else if (isX) { %>X<% } else { %>O<% } %></span><% } %>"),

    initialize: function() {
        var that = this;
        this.model.on('change', function() {
            that.render.call(that);
        });
    },

    squareClick: function() {
        this.model.playerMove();
    },

    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    }
});