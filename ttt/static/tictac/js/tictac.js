
define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {

    Board = Backbone.Model.extend({
      url: '/game/board/'
    });

    BoardView = Backbone.View.extend({

        initialize: function(attributes, options) {

            _.bindAll(this, 'render');

            this.listenTo(this.model, 'change', this.render);
            this.model.fetch({
            });
        },

        render: function() {
          console.log('new state: ' + this.model.get('state'));
          var template = _.template(
              $( "script.template" ).html()
          );
          $( ".board-holder" ).html(
            template( this.model )
          );




        }

    });

    var didLaunch = function() {
        console.log('hi, it launched!');
        $('#ok').show();
        $('#fail').hide();

        var board = new Board();
        var boardView = new BoardView({ model: board });

    };

    return {
      didLaunch: didLaunch
    };
});
