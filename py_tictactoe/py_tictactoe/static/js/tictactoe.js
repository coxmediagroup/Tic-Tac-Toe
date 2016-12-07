var TicTacToe = {
	img_map: {
		1: "cell_X.png",
		2: "cell_O.png"
	},
	human_data: "{{ human_data }}",
	computer_data: "{{ computer_data }}",

	move_human: function(cell) {
		if (cell.attr('data')) {
			alert('This cell has been taken already!');
		} else {
			this._show_move(cell, this.human_data);
			this._post_move(cell);
		}
	},
	move_computer: function(cell) {
		if (cell.attr('data')) {
			alert('This cell has been taken already!');
		} else {
			this._show_move(cell, this.computer_data);
		}
	},
	_show_move: function(cell, data) {
		cell.append("<img src='"+SITE_IMG_BASE+this.img_map[data]+"'/>");
		cell.attr("data",data);
	},
	_post_move: function(cell) {
		$.get('move',{cell: cell.attr("id").substring(5), _dc: Math.random()})
			.done(function(data){
				if (data.error) {
					alert(data.error.message);
					if (data.error.critical)
						window.location = "/";
				} else {
					if (data.move) {
						TicTacToe.move_computer($("#cell_"+data.move.cell));
					}
					if (data.status == "human win") {
						$('#reset').hide();
						$('#status_win').css('display','inline-block');
					} else if (data.status == "computer win") {
						$('#reset').hide();
						$('#status_lose').css('display','inline-block');
					} else if (data.status == "cat win") {
						$('#reset').hide();
						$('#status_tie').css('display','inline-block');
					} else if (data.status) {
						alert(data.status);
					}

				}
			});
	}
};
