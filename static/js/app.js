var userFontClass = "fa-linux";
var computerFontClass = "fa-windows";

/* Inserts the User's Selected piece into the box specified. */
var insertPiece = function(element) {

	// Submit the Piece Selection to the Server

};


$(document).ready(function() {

	// Display all Game Pieces upon initial page load.
	$('.piece-box').each(function(i, obj) {

		// Determine the Piece that belongs to this Box.
		var player = $(obj).attr('data-piece');

		// Insert Player's Piece
		if ( player == 1 ) {
			var gamePiece = $(document.createElement("i"))
						.addClass("fa fa-5x")
						.addClass(userFontClass);
		}

		// Insert Computer's Piece
		else if ( player == -1 ) {
			var gamePiece = $(document.createElement("i"))
						.addClass("fa fa-5x")
						.addClass(computerFontClass);
		}

		// Disable User Selection of this Box
		$(obj).append(gamePiece).addClass('disabled');

	});

	// Insert a Game Piece when a User selects a position on the Game Board. 
	$('.piece-box').click(function() {
		$(this).has('i').length 
			? console.log("This cell already contains a game piece.")
			: insertPiece(this);
	});

	var csrftoken = $.cookie('csrftoken');
	console.log("CSRF Token: " + csrftoken);

});
