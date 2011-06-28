$(document).ready(function(){
	
	var game = null;
	var playerIsX = true;
	
	// start game
	$('.btn-play').click(function(){
		if($(this).hasClass('x')) {
			playerIsX = true;
		} else {
			playerIsX = false;
		}
		$('#options').fadeOut(function(){
			game = new TicTacToe.game();
			game.init('game-canvas', playerIsX, gameOver, function(){
				$('#game-area').fadeIn();
			});
		});
	});
	
	// this is called when the game ends
	function gameOver(code) {
		switch(code) {
		case TicTacToe.WIN:
			msg = 'This isn\'t possible!';
			break;
		case TicTacToe.LOSE:
			msg = 'You Lose.';
			break;
		case TicTacToe.TIE:
			msg = 'It\'s a tie!';
			break;
		}
		msg += ' Play Again?';
		$('<div />').html(msg).dialog({
			title:'Game Over',
			position:'top',
			modal:true,
			buttons: {
				'Yes': function() { $(this).dialog('close');game.newGame(playerIsX, null); },
				'No': function() { $(this).dialog('close');reset(); }
			}
		});
	}
	
});

function reset() {
	$('#game-area').fadeOut(function(){
		$('#options').fadeIn();
	});
}

// taken from https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
