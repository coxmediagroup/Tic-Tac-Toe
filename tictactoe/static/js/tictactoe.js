/**
 * Progressive enhancements for the bare-bones game UI.
 * @param selector {string} - selector for the board form (must contain "input[name=cell]"s)
 * @param [endpoint] {string} - url to post marks to (defaults to board's action attribute
 * @param [jquery] - explicitly choose the jQuery object to use (defaults to window.jQuery)
 */
function Board(selector, endpoint, jquery) {
  if (!selector) {
    throw new Error("selector is a required parameter.");
  }

  var $ = jquery || window.jQuery,
    $board = $(selector),
    url = endpoint || $board.attr('action');

  $board
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
          csrfmiddlewaretoken: $board.find('[name=csrfmiddlewaretoken]').val(),
          cell: $(this).val()
        }
      }).done(function (data) {
          console.log(data);
      });
    });


}