
define([
    'jquery',
    'underscore',
    'backbone',
    'bootstrap'
], function($, _, Backbone) {

    /*
     * Board model */

    Board = Backbone.Model.extend({
      url: '/game/board/',
      play_url: '/game/play/',
    });


    /*
     * Board view */

    BoardView = Backbone.View.extend({

        initialize: function(attributes, options) {

            _.bindAll(this, 'render');
            _.bindAll(this, 'space_clicked');

            // Update our board when our model changes.
            this.listenTo(this.model, 'change', this.render);

            // ... and make sure it does.
            this.model.fetch();
        },

        render: function() {
          var template = _.template(
              $( "script.template" ).html()
          );
          $( ".board-holder" ).html(
            template( this.model )
          );

          // If it's open, watch for clicks on the space.
          $(".playable").click(this.space_clicked);
        },

        space_clicked: function(e) {

          // If the game is over, then it's _over_. Sorry.
          //
          if (this.model.attributes['game_over']) {
            return;
          }

          // If a space is clicked, play it.
          var target = e.target;
          var pos = $(target).data('position');

          while ((pos === undefined) && (target)) {
            target = target.parentElement;
            pos = $(target).data('position');
          }

          if (!target) {
            // This shouldn't really happen;
            return;
          }


          var model = this.model;

          // After we tell the server what to play, and it comes
          // back with (hopefully) good news, update our model to
          // update our view. This routine just throws caution to
          // the wind; if the server blows up, we have bigger problem
          // than a silly TTT game.
          //
          $.ajax({
              url: this.model.play_url,
              data: {
                player: this.model.attributes['next_player'],
                position: pos
              },
              type: 'POST',
            }
          ).done(function() { model.fetch(); });

        }
    });


    var didLaunch = function() {
        var board = new Board();
        var boardView = new BoardView({ model: board });

        // If we start a new game, submit the new game form!
        //
        $('#newGameModal').on('hidden.bs.modal', function (e) {
          console.log(e);
          var form = $('form[name="newGameForm"]');
          form.submit();
        });

        // Set up event handler for choosing a symbol in the new game
        // page.
        //
        $('.symbol-choices span[class="tictac"]').click(function(e) {
          var target = e.target;
          while (target && (target.className != 'symbol-choices')) {
            target = target.parentElement;
          }
          var inputtarget=$(target).data('input-target');
          var displaytarget=$(target).data('display-target');
          var value = $(e.target).data('value');

          $('#' + inputtarget).val(value);
          $('#' + displaytarget).html(value);

        });
    };

    return {
      didLaunch: didLaunch
    };
});
