!(function () {
  "use strict";

  var CROSS = true,
      NAUGHT = false,
      EMPTY = null,
      MARK = {};
  MARK[CROSS] = "X";
  MARK[NAUGHT] = "O";

  /**
   * Progressive enhancements for the bare-bones game UI.
   * @param selector {string} - selector for the board form (must contain "input[name=cell]"s)
   * @param [endpoint] {string} - url to post marks to (defaults to board's action attribute
   * @param [jquery] {jQuery} - explicitly choose the jQuery object to use (defaults to window.jQuery)
   */
  function Board (selector, endpoint, jquery) {
    if (!selector) {
      throw new Error("selector is a required parameter.");
    }

    var $ = jquery || window.jQuery,
        $board = $(selector),
        $body = $(document.body),
        url = endpoint || $board.attr('action'),
        /**
         * Collection of internal methods for Board.
         * @access private
         */
        __ = {
          /**
           * Logs a message to the console, but only when the
           * hash is "#debug" and console.log is available to the client.
           * @param message {object} - the data to be passed to console.log
           */
          log: function (message) {
            if (console && console.log && window.location.hash === '#debug') {
              console.log(message);
            }
          },
          /**
           * Updates the state of the Board cells on cell data and win
           * conditions recieved from the server.
           * @param cells {Array} - array of cell states
           */
          updateBoard: function (cells) {
            $.each(cells, function (idx, value) {
              $board.find("[name=cell]").each(function () {
                var $btn = $(this),
                    idx = parseInt($btn.val());

                if (cells[idx] !== EMPTY) {
                  $btn.parent().text(MARK[cells[idx]]);
                }
              });
            })

          },
          /**
           * Top-level "macro" method that consumes data from the server,
           * performs all work to manage game state and render
           * feedback for the user.
           * @param data
           */
          tick: function (data) {
            $body.removeClass("game-start"); // clears the instructional message if present.
            this.updateBoard(data.cells);
            if (data.gameIsOver) {
              $body.addClass("game-end");
              // remove any inputs to prevent interaction with the board
              // after the game is over.
              $board.find("[name=cell]").remove();
              // sets the "win/draw" message
              $(".game-end>h1>span", "#header").text(data.error);
            }
          }
        };

    !(function ($form) {
        /**
         * Event binding.
         * Binds up ajax events, and callbacks to the various DOM elements we're
         * interacting with.
         * Locked this code up inside a closure to prevent us from being tempted to
         * reach inside from the main Board scope.
         */
        $form
          .submit(function (event) {
            event.preventDefault();
          })
          .find('[name=cell]').click(function (event) {
            event.preventDefault();

            $.ajax({
              url: url,
              type: 'POST',
              cache: false,
              data: {
                /**
                 * TODO: if/when we need to POST to from multiple scripts hook into
                 * the jQuery ajax events and send the token as a X-Header from a
                 * common script.
                 */
                csrfmiddlewaretoken: $form.find('[name=csrfmiddlewaretoken]').val(),
                cell: $(this).val()
              }
            })
            .done(function (data) {
                __.tick(data);
            });
          });
    }($board));
  }

  // export the Board to the tictactoe namespace
  window.tictactoe = window.tictactoe || {};
  window.tictactoe.Board = Board;
}());