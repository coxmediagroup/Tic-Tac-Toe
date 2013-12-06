(function($) {
	"use strict";

	// normally it would need csrf protection for POSTing json to
	// views, but I ran out of time to set that up


	var waiting = false;

	$.fn.create_game = function(){
		this.on('click', make_move);
	};

	var process_move = function process_move(){
		// callback for the posts
		alert('got callback');
		waiting = false;
	};

	var get_board_state = function get_board_state() {
		var data = {
			"m1": $('.m1')[0].data('state'),
			"m2": $('.m2')[0].data('state'),
			"m3": $('.m3')[0].data('state'),
			"m4": $('.m4')[0].data('state'),
			"m5": $('.m5')[0].data('state'),
			"m6": $('.m6')[0].data('state'),
			"m7": $('.m7')[0].data('state'),
			"m8": $('.m8')[0].data('state'),
			"m9": $('.m9')[0].data('state'),
		}
		return data;
	};

	var make_move = function make_move(){
		if (waiting) {
			return false;
		}
		// gather game data
		var gamedata = get_board_state();

		// send it off to be processed
		$.ajax({
			type: "POST",
			url: window.location,
			data: gamedata,
			success: process_move,
			dataType: 'json',
			beforeSend: function(xhr, opt){
				// this is not the best way of preserving the game
				// state from clicking quickly, nor is it exactly
				// thread-safe per say, it would need more work
				if(waiting) {
					return false;
				}
				else {
					waiting = true;
				}
			}
		});
	};

	$(function() {
		$(".gamegrid").create_game();
	});

}(jQuery));

