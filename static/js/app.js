var userFontClass = "fa-linux";

/* Inserts the User's Selected piece into the box specified. */
var insertPiece = function(element) {
	var gamePiece = $(document.createElement("i"))
						.addClass("fa fa-5x")
						.addClass(userFontClass);

	$(element).append(gamePiece);
}

$(document).ready(function() {

	// Insert a Game Piece when a User selects a position on the Game Board. 
	$('#game-table tbody tr td').click(function() {
		$(this).has('i').length 
			? notifyUser("Please select an empty box.")
			: insertPiece(this);
	});

});