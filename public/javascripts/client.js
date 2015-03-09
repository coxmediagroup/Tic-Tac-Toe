$(function() {
	
	var cached = undefined;
	
	$.get('/reset');
	
	$('.cell').click(function() {
		var $this = $( this );
		var cell = $this.data('cell');
		$.getJSON('/select/' + cell + '/x', function(data) {
			if (cached != data) {
				cached = data;
				updateBoard(data.board);
			}
		});
	});
	
	function updateBoard(board) {
		for (var i in board) {
			if (board[i] != undefined) {
				$('span[data-cell="' + i + '"]').html(board[i]);
			}
		}
	}
});