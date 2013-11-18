var userFontClass = "fa-linux";

/* Inserts the User's Selected piece into the box specified. */
var insertPiece = function(element) {

	// Create the Game Piece Element
	var gamePiece = $(document.createElement("i"))
						.addClass("fa fa-5x")
						.addClass(userFontClass);

	// Insert and Disable the box.
	$(element)
		.append(gamePiece)
		.addClass('disabled');


};


$(document).ready(function() {

	// Display all Game Pieces upon initial page load.
	$('.piece-box').each(function(i, obj) {
		console.log("Piece: " + $(obj).attr('data-piece'));
	});

	// Insert a Game Piece when a User selects a position on the Game Board. 
	$('.piece-box').click(function() {
		$(this).has('i').length 
			? console.log("This cell already contains a game piece.")
			: insertPiece(this);
	});


});
