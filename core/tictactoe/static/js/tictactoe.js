(function($) {
	"use strict";

	// normally it would need csrf protection for POSTing json to
	// views, but I ran out of time to set that up


	var waiting = false;

	$.fn.create_game = function(){
		this.on('click', make_move);
	};

	var process_move = function process_move(data, status, xhr){
		$('#m1').data('state', data["m1"]);
		$('#m1').html(data["m1"]);
		$('#m2').data('state', data["m2"]);
		$('#m2').html(data["m2"]);
		$('#m3').data('state', data["m3"]);
		$('#m3').html(data["m3"]);
		$('#m4').data('state', data["m4"]);
		$('#m4').html(data["m4"]);
		$('#m5').data('state', data["m5"]);
		$('#m5').html(data["m5"]);
		$('#m6').data('state', data["m6"]);
		$('#m6').html(data["m6"]);
		$('#m7').data('state', data["m7"]);
		$('#m7').html(data["m7"]);
		$('#m8').data('state', data["m8"]);
		$('#m8').html(data["m8"]);
		$('#m9').data('state', data["m9"]);
		$('#m9').html(data["m9"]);
		$('#game-message').html(data["status"]);
		$('#gametoken').data('gamestate', data["gamestate"])
		waiting = false;
	};

	var get_board_state = function get_board_state() {
		var data = {
			"m1": $('#m1').data('state'),
			"m2": $('#m2').data('state'),
			"m3": $('#m3').data('state'),
			"m4": $('#m4').data('state'),
			"m5": $('#m5').data('state'),
			"m6": $('#m6').data('state'),
			"m7": $('#m7').data('state'),
			"m8": $('#m8').data('state'),
			"m9": $('#m9').data('state'),
		}
		return data;
	};

	var make_move = function make_move(){
		if (waiting) {
			return false;
		}
		// gather game data
		var gamedata = get_board_state();
		gamedata["move"] = $(this).attr("id");
		gamedata["token"] = $("#gametoken").data("token");
		gamedata["gamestate"] = $("#gametoken").data("gamestate")

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
		$(".movespot").create_game();
	});

}(jQuery));

