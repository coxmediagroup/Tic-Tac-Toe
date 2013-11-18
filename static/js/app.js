// Defines Game Pieces (Icons) used in the Game
var userFontClass = "fa-linux",
  computerFontClass = "fa-windows";

// Submits the User's selection
function insertPiece() {
  "use strict";
  if (!$(this).has('i').length) {
    var box = $(this).attr('id'),
      selection = $(document.createElement("input"))
                      .attr("type", "hidden")
                      .attr("name", "selection")
                      .attr("value", box);
    $('#selection-form').append(selection);
    $('#selection-form').submit();
  }
}

// Render the Game Piece
function renderGamePiece() {
  "use strict";
  var player = parseInt($(this).attr('data-piece'), 0),
    gamePiece = $(document.createElement("i"))
                  .addClass("fa fa-5x");
  if (player === 1) {
    gamePiece.addClass(userFontClass);
    $(this).append(gamePiece).addClass('disabled');
  } else if (player === -1) {
    gamePiece.addClass(computerFontClass);
    $(this).append(gamePiece).addClass('disabled');
  }
}

$(document).ready(function () {
  "use strict";
  $('.piece-box').each(renderGamePiece);
  $('.piece-box').click(insertPiece);
});
