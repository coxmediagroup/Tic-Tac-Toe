$(function() {
	
	var cached = undefined;
	
	$.get('/reset');
	
	$('.cell').click(function() {
		var $this = $( this );
		var cell = $this.data('cell');
		$.getJSON('/select/' + cell + '/X', function(data) {
			if (cached != data) {
				cached = data;
				if (data.winner) {
					/* handle winner */
					$('h2#message').html(data.winningPlayer + ' has won the game! Refresh to replay').addClass('green');
					$('.cell').unbind('click');
				}
				else if (!data.hasMovesLeft) {
					/* no more moves */
					$('h2#message').html('There are no moves left. Refresh to replay').addClass('red');
					$('.cell').unbind('click');
				}
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