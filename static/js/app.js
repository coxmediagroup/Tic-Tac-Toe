// Defines Game Pieces (Icons) used in the Game
var userFontClass = "fa-linux",
  computerFontClass = "fa-windows";

// Submits the User's selection
function insertPiece(event) {
  if (!$(this).has('i').length) {
    var box = $(this).attr('id'),
      selection = $(document.createElement("input"))
                      .attr("type", "hidden")
                      .attr("name", "selection")
                      .attr("value", box);
    $('#selection-form').append(selection);
    $('#selection-form').submit();
  };
};

// Render the Game Piece
function renderGamePiece(i, obj) {
  var player = parseInt($(obj).attr('data-piece'));
  if ( player === 1 ) {
    var gamePiece = $(document.createElement("i"))
                      .addClass("fa fa-5x")
                      .addClass(userFontClass);
    $(obj).append(gamePiece).addClass('disabled');
  } else if ( player === -1 ) {
    var gamePiece = $(document.createElement("i"))
                      .addClass("fa fa-5x")
                      .addClass(computerFontClass);
    $(obj).append(gamePiece).addClass('disabled');
  }
};

$(document).ready(function() {
  $('.piece-box').each(renderGamePiece);
  $('.piece-box').click(insertPiece);
});
