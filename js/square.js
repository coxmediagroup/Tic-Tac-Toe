var Square = Backbone.Model.extend({
    defaults: {
        isX: true
    }
});

var SquareView = Backbone.View.extend({
    tag: "div",
    className: "square",
    template: _.template("<span><% if (isX) { %>X<% } else { %>O<% } %></span>"),

    init: function() {
        this.model.on('change', this.render);
    },

    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    }
});