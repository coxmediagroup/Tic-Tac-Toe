$(document).ready(function(){
	$('#waiting')
    .hide()
    .ajaxStart(function() {
        $(this).show(); //hide the waiting animation on page load
    })
    .ajaxStop(function() {
        $(this).hide();
    })

	$('.first_move').click(function(e){
		target = e.target;
		$(target).unbind('click');
		$(target).css('font-weight','bold');
		$.ajax({
			type: 'POST',
			url: '/tictactoe/pick/' + $(this).attr('order'), // when the first mover is picked, make an ajax call and wait for the response
			success: function(response){
				if(typeof(response.computer_move) != 'undefined'){
					// if the first mover is the computer, fill the box specified in the computer response 
					$('.row div[index="'+response.computer_move+'"]').css('background-image', 'url(tictactoe/media/images/o.gif)');
				}
				// initialize the board so it can listen for clicks
				init_board();
			}
		})
	});
	
	function init_board(){
		$('.row div').click(function(){
			$(this).css('background-image', 'url(tictactoe/media/images/x.gif)');
			$.ajax({
				type: 'POST',
				url: '/tictactoe/move/' + $(this).attr('index'),
				beforeSend: function(){
					$('.row div').unbind('click'); //disable the listener during the ajax call to avoid multiple calls being sent
				},
				success: function(response){
					if(typeof(response.computer_move) != 'undefined'){
						$('.row div[index="'+response.computer_move+'"]').css('background-image', 'url(tictactoe/media/images/o.gif)');
					}
					if(response.message == 'game_over'){
						if(typeof(response.winner) != 'undefined'){
							if(response.winner == '1')
								alert('You Won!');
							if(response.winner == '2')
								alert('You lost!');
						}
						else
							alert('Draw!');
						$('.row div').unbind('click');
						$('#game_over').show();
					}
					else
						init_board(); // if the game is not over, reinitialize the board.
				}
			})
		});
	}
});