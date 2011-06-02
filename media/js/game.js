function game(){
	
}
$(document).ready(function(){
	$('.first_move').click(function(){
		$.ajax({
			type: 'POST',
			url: '/tictactoe/pick/' + $(this).attr('order'),
			success: function(response){
				if(response.computer_move)
					$('.row div[index="'+response.computer_move+'"]').css('background-image', 'url(tictactoe/media/images/o.gif)');
				else{
					alert(response.message);
				}
			}
		})
	});
	$('.row div').click(function(){
		$(this).css('background-image', 'url(tictactoe/media/images/x.gif)');
		$.ajax({
			type: 'POST',
			url: '/tictactoe/move/' + $(this).attr('index'),
			success: function(response){
				if(response.computer_move)
					$('.row div[index="'+response.computer_move+'"]').css('background-image', 'url(tictactoe/media/images/o.gif)');
				if(response.message == 'game_over')
					alert('winner: '+response.winner)
			}
		})
	});
});