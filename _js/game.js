var selected_icon,winning_line,gameover = false, player1_selected_icon,player2_selected_icon, setupuser = "player1",currentPlayer = null,computer_playing = false,contin = true,p1_probablilty = [],p2_probablilty = [],turn_count = 0,currentGame;

if(localStorage.getItem('scoreboard') == '' || localStorage.getItem('scoreboard') == null){
	var scores = [];
}else{
	var scores = localStorage.getItem('scoreboard');
}

var waystowin = {
	0 : ['a1','b1','c1'],
	1 : ['a1','a2','a3'],
	2 : ['a1','b2','c3'],
	3 : ['b1','b2','b3'],
	4 : ['c1','c2','c3'],
	5 : ['c1','b2','a3'],
	6 : ['a2','b2','c2'],
	7 : ['a3','b3','c3']
}

function Game (players,icons){
	/* CLEAR OUT PREVIOUS GAMES */
	localStorage.removeItem('playerturn');
	/* SET UP NEW GAME */
	localStorage.setItem('playerturn', 'player1');
	this.numplayers = players;
	this.x = icons.player1;
	this.o = icons.player2;
	this.player1moves = [];
	this.player2moves = [];
	console.log('game started');
}

Game.prototype.checkWinner = function(){
	var nowinner = true;

	for(var i in waystowin){
		// LOOP THROUGH ALL WINNING SCENARIOS
		var blocks = 0;
		if(!nowinner){

		}else{
			for(var n in waystowin[i]){
				// GET INDIVIDUAL BLOCKS FROM WINNING SCENARIO
				var blockid = waystowin[i][n];
				var blockval = $('#'+blockid).html();
				// IF THE CURRENT USER HAS A BLOCK WITH IN THIS SCENARIO ADD 1
				if(blockval === selected_icon){
					blocks = blocks + 1;
				}
				// IF THE CURRENT SCENARIO REACHES THREE THE USER HAS WON
				if(blocks === 3){
					nowinner = false;
					winning_line = waystowin[i];
				}else{
					nowinner = true;
				}
			}
		}
	}
	if(!nowinner){
		return true;
	}else{
		if(turn_count == 9){
			gameover == true;
			winning_line = 'draw';
			$('#no-winner').show();
		}
		return false;
	}	
}
Game.prototype.drawLine = function(line){
	gameover = true;
	var playername = localStorage.getItem(currentPlayer+'name');
	$('.grid-block').addClass('losing-block');

	for(var o in winning_line){
		$('#'+winning_line[o]).addClass('winning-block');
	}
	$('#winner-message').html(playername+' wins!');
}
/* AI FUNCTIONS */
var computer = {
	select_icon : function(){
		$('#icon-selection a:not([data-icon="'+localStorage.getItem('player1icon')+'])')[2].click();
	},
	select_name : function(){
		$('#playename').val("XO / Computer");
		setTimeout(function(){
			$('#done-name').click();
		},300);
	},
	check_probability : function(){
		var nowinner = true;
		p1_probablilty = [];
		var p1_icon = localStorage.getItem('player1icon');
		var p2_icon = localStorage.getItem('player2icon');
		var selected = '';

		for(var i in waystowin){
			// LOOP THROUGH ALL WINNING SCENARIOS
			var spots = [];
			var p1_chances = 0;
			var found = false;
			var y = [];

			for(var n in waystowin[i]){
					// GET INDIVIDUAL BLOCKS FROM WINNING SCENARIO
				var blockid = waystowin[i][n];
				var sblock = $('#'+blockid);
				var blockval = sblock.html();
				if(blockval === p1_icon){
					//block is filled in
					p1_chances = p1_chances + 1;
				}
				y.push(blockid);
			}
			var x = [
				{
					id : y,
					chance : p1_chances
				}
			];
			p1_probablilty.push(x);
		}
		computer.select_block();
	},
	select_block : function(player){
		var keeploop = true;
		var computer_selection = '';
		var block = '';
		var highestchance = [
			{
				index : 0,
				id : '',
				cval : 0
			}
		];
		
		for(var w in p1_probablilty){
			if(p1_probablilty[w][0].chance > highestchance[0].cval){
				highestchance = [
					{
						index : w,
						id : p1_probablilty[w][0].id,
						cval : p1_probablilty[w][0].chance
					}
				];
			}
		}
		var line = parseInt(highestchance[0].index);
		var loopthrough = 0;

		for(var g in waystowin[line]){
			var el = waystowin[line][g];
			if(keeploop){
				if($('#'+el).html() == ''){
					keeploop = false;
					$('#'+el).click();
				}else{
					loopthrough = loopthrough + 1;
				}
			}
		}
		// if the computer can't figure out a move, go through the winning scenarios and fill it
		if(loopthrough === 3){
			for(var i in waystowin){
				if(contin){
					for(var n in waystowin[i]){
							// GET INDIVIDUAL BLOCKS FROM WINNING SCENARIO
						var blockid = waystowin[i][n];
						var sblock = $('#'+blockid);
						var blockval = sblock.html();
						if(blockval === ''){
							sblock.click();
							contin = false;
						}
					}
				}
			}
		}
	}
}
/* SET UP DATA FOR GAME */
var setupGame = {
	init : function(){
		var number_plys = localStorage.getItem('numplayers');
		if(number_plys == 1){
			computer_playing = true;
		}
		/* CLEAR OUT PREVIOUS GAME */
		$('#game-board').removeClass('in-progress');
		var checkuser1 = localStorage.getItem('player1icon');
		var checkuser2 = localStorage.getItem('player2icon');
		/* SET UP NEW GAME */
		var numberplayers = localStorage.getItem('numplayers');

		// check if there's a game in progress
		if(!checkuser1){
			setupuser = "player1";
		}else if(!checkuser2){
			setupuser = "player2";
		}
		
		if(!checkuser1 || !checkuser2){
			this.nameit();
		}else{
			setupGame.fillinfo();
		}
	},
	cleargame : function(){
		localStorage.removeItem('numplayers');
		localStorage.removeItem('player1name');
		localStorage.removeItem('player1icon');
		localStorage.removeItem('player2name');
		localStorage.removeItem('player2icon');
	},
	nameit : function(){
		$('#playercard h5').html("Enter "+setupuser+"'s Name");
		$('#icon-selection h5').html("Select "+setupuser+"'s Icon");
		$('#playercard').show();

		if(computer_playing === true && setupuser === "player2"){
			computer.select_name();
		}
	},
	icons : function(){
		$('#playercard').hide();
		$('#icon-selection').show();

		if(computer_playing === true && setupuser === "player2"){
			computer.select_icon();
		}
	},
	fillinfo : function(){
		for(var i = 1; i<3; i++){
			$('#player'+i+'-info a').addClass(localStorage.getItem('player'+i+'icon'));
			$('#player'+i+'-info .user-name').html(localStorage.getItem('player'+i+'name'));
		}
		if(setupuser === 'player2'){
			// both players have filled in info
			startGame();
		}else{
			// only player one is ready
			if(localStorage.getItem('player2icon') != ''){
				startGame();
			}else{
				setupuser = "player2";
				setupGame.nameit();
			}
		}
	}
}
/* ALL INFORMATION ABOUT USERS IS CAPTURED, READY TO START A GAME */
var startGame  = function(){
	$('#game-board').addClass('in-progress');
	var playericons = {
		player1 : localStorage.getItem('player1icon'),
		player2 : localStorage.getItem('player2icon')
	}
	currentGame = new Game(2,playericons);

}

/* init game setup to gather info on users */
$(document).ready(function(){
	setupGame.init();
});

/* EVENT LISTENERS */
$('#icon-selection a').on('click',function(event){
	event.preventDefault();
	event.stopPropagation();
	var obj = $(this);
	var icon = obj.data('icon');
	localStorage.setItem(setupuser+'icon',icon);
	$('#error').html('');

	if(setupuser === 'player1'){
		setupuser = 'player2';
		setupGame.nameit();
		$('#icon-selection').hide();
	}else{
		if(icon === localStorage.getItem('player1icon')){
			$('#error').html('You can not have the same icon as the other player');
		}else{
			setupGame.fillinfo();
			$('#icon-selection').hide();
		}
	}
});
$('#clear-game').on('click',function(event){
	event.preventDefault();
	window.location.reload();
});
$('.startnew,#logo').on('click',function(event){
	event.preventDefault();
	setupGame.cleargame();
	window.location = 'index.html';
});
$('#done-name').on('click',function(event){
	event.preventDefault();
	event.stopPropagation();
	var pname = $('#playename').val();
	localStorage.setItem(setupuser+'name',pname);
	$('#playename').val('');
	setupGame.icons();
});

$('.grid-block').on('click',function(event){
	event.preventDefault();
	var obj = $(this);
	var block = obj.attr('id');
	currentPlayer = localStorage.getItem('playerturn');
	if(obj.html() === '' && gameover == false){
		// CHECK IF THE BLOCK IS EMPTY AND THE GAME IS NOT OVER
		switch(currentPlayer){
			case "player1":
				selected_icon = currentGame.x;
				// KEEP TRACK OF THE USERS MOVES
				currentGame.player1moves.push(block);
				var nextplayer = "player2";
			break;
			case "player2":
				selected_icon = currentGame.o;
				// KEEP TRACK OF THE USERS MOVES
				currentGame.player2moves.push(block);
				var nextplayer = "player1";
			break;
		}
		obj.addClass(selected_icon).html(selected_icon);

		turn_count++;

		var victory = currentGame.checkWinner(block);

		if(!victory){
			$('.active-player').removeClass('active-player');
			localStorage.setItem('playerturn',nextplayer);
			currentPlayer = nextplayer;
			$('#'+nextplayer+'-info').addClass('active-player');
			if(nextplayer === 'player2' && computer_playing === true){
				contin = true;
				computer.check_probability();
			}
		}else{
			currentGame.drawLine(winning_line);
		}
	}else{
		console.log('that block is not available');
	}	
});