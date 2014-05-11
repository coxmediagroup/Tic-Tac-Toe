function toggleBoard(cell){
	var selector = "#"+cell;
	if($(selector).hasClass('selected')){
		$(selector).text("");
		$(selector).removeClass('selected');
	}
	else {
		$(selector).text("X");
		$(selector).addClass('selected');
	}
}