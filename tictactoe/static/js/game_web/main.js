//game_web main javascript file

//Constructor for Tic-Tac-Toe game
function tictactoe() {
	//Constants
	this.MAX_SPACES = 9;
	this.board = this.initBoard();
	this.lastSpaceTaken = null;
	//Get the first turn upon initialization
	//Values will either be 1 for true or 0 for false
	this.playersTurn = this.firstTurn();
	// Used for checking for stalemates
	this.spacesTaken = 0;
	this.clearBoard();

}

// Add the user's choice to the board
// We have to parse the element ID to get the index of the
// board the user chose
tictactoe.prototype.addUserChoice = function(elementID) {
	// Format for element ID is cell-XY
	var indexString = (elementID.split('-'))[1];
	// Parse the indexes into two separate integers
	var xCoord = parseInt(indexString[0]);
	var yCoord = parseInt(indexString[1]);
	// Update the board to the correct spot
	this.board[xCoord][yCoord] = "o";
	// Update the lastSpaceTaken coordinates
	this.lastSpaceTaken = new Array(2);
	this.lastSpaceTaken[0] = xCoord;
	this.lastSpaceTaken[1] = yCoord;
	// Increment the number of spaces that are taken
	this.incrementSpacesTaken();
	this.checkWin();
}

tictactoe.prototype.checkStalemate = function() {
	return (this.MAX_SPACES === this.spacesTaken);
}

// Check if the game has been won yet
// It takes at least 5 turns for someone to win in Tic-Tac-Toe,
// so don't waste the time checking for a win if 5 turns (or spaces)
// haven't been taken
// Check if it's less than 5 because we increment spacesTaken before
// this function is called
tictactoe.prototype.checkWin = function() {
	if(this.spaceTaken < 0)
		return false;
	else{
		var game = this;
		$.ajax({
			type: "POST", 
			url: "checkWin", 
			dataType: "json",
			data: {
				board: JSON.stringify(this.board),
				lastSpaceTaken: JSON.stringify(this.lastSpaceTaken),
			},
			success: function(results){
				//resultsJSON = $.parseJSON(results);
				//alert(results['win']);
				var win = results['win'];
				if(win == true){
					stopGame();
					if(game.playersTurn){
						displayStatus("You won!", "good");
					}
					else{
						displayStatus("Sorry...maybe next time...", "bad");
					}
					setTimeout(function(){
							initGame();
						}, 3000);
				}
				else{
					if(game.checkStalemate() == true){
						stopGame();
						displayStatus("Stalemate!", "normal");
						setTimeout(function(){
							initGame();
						}, 3000);
						win = true;
				}
				if(win == false){
					game.nextTurn();
					if(game.playersTurn == true)
						displayStatus("Your turn...", "good");
					else{
						game.takeAITurn();
					}
				}
			}
			},
			error: function(){
				displayStatus("Something went wrong...", "error");
			}
		});
	}
}

// Clear the board and start a new game
tictactoe.prototype.clearBoard = function() {
	$('td').removeClass("xTaken oTaken");
}

// Determine who goes first 
tictactoe.prototype.firstTurn = function() {
	//If the number is even, the AI gets the first turn
	//Use 0 to 99 so the number of possibilities for even
	//and odd number are equal
	//Including 100 would add one more possibility for the
	//resulting number to be even
	var randTurn = Math.floor(Math.random() * 99) % 2;
	if(randTurn > 0)
		return true;
	else
		return false;
}

// Increment turns taken
tictactoe.prototype.incrementSpacesTaken = function() {
	this.spacesTaken++;
}

// Initialize the TicTacToe board (2D Array)
tictactoe.prototype.initBoard = function() {
	var board = Array(3);
	for(var i = 0; i < board.length; i++)
		board[i] = Array(3);
	return board;
}

// Determine the next turn
tictactoe.prototype.nextTurn = function() {
	if(this.playersTurn)
		this.playersTurn = false;
	else
		this.playersTurn = true;
}

// Set the last space that was taken
// Will make checkWin algorithm and AI more efficient
tictactoe.prototype.setLastSpaceTaken = function(spaceTaken) {
	this.lastSpaceTaken = spaceTaken;
}

// Run funtion for Tic-Tac-Toe game
tictactoe.prototype.run = function(){

}

// Have the AI take its turn
tictactoe.prototype.takeAITurn = function() {
	displayStatus("Opponent's turn...", "bad");
	// Cant use 'this' in ajax call
	var game = this;
	$.ajax({
			type: "POST", 
			url: "AI_turn", 
			dataType: "json",
			data: {
				board: JSON.stringify(this.board),
				lastSpaceTaken: JSON.stringify(this.lastSpaceTaken),
			},
			success: function(results){
				// Slow down the game a little
				setTimeout(function(){
					var coords = results['chosenCoords'];
					// Update the board with the AI decision
					game.board[coords[0]][coords[1]] = "x";
					// Reflect that decision on the UI
					var elemID = "#cell-" + coords[0] + coords[1];
					$(elemID).addClass("xTaken");
					// Increment the number of spaces that are taken
					game.incrementSpacesTaken();
					// Update lastSpotTaken
					game.setLastSpaceTaken(coords);
					game.checkWin();
				}, 1000);
			},
			error: function(){
				displayStatus("Something went wrong...", "error");
			}
		});
}

// Display a message to the user
var fadeTimeout;

function displayStatus(message, type, noFadeOut) {
	var fadeOutTime = 400;
	// Colors for status indicator
	var statusColors = {
		"good": "green",
		"bad": "red", 
		"error": "orange", 
		"normal": "#85ADFF"
	};
	clearTimeout(fadeTimeout);
	if((noFadeOut===undefined)){
		$('#status').fadeOut(fadeOutTime, function(){
			$('#status').html(message)
			$('#status').css("background-color", statusColors[type]);
		});
		$('#status').fadeIn();
		fadeTimeout = setTimeout(function(){
			$('#status').fadeOut();
		}, 5000);
	}
	else{
		$('#status').fadeIn();
		$('#status').html(message)
		$('#status').css("background-color", statusColors[type]);		
	}
}

// Global Tic-Tac-Toe object 
var ttt_game;

function initGame(countDown){
	ttt_game = new tictactoe();
	if(countDown===undefined)
		countDown = 3;

	var messageToUser = "Game starts in " + countDown + "..."
	// Display countdown to user until countDown variable == 0
	if(countDown != 0){
		displayStatus(messageToUser, "normal", true);
		setTimeout(function(){
			initGame(countDown-1);
		}, 1000);
	}
	else
	{
		runGame();
	}
		
}

// Display introduction messages to user upon first load
function intro() {
	var messageToUser = "Welcome to the Cox Media Tic-Tac-Toe Challenge!"
	displayStatus(messageToUser, "normal");
	messageToUser = "Click on a space to take it!";
	setTimeout(function(){
		displayStatus(messageToUser, "normal");
		setTimeout(function(){
			initGame();
		}, 3000);
	}, 3000);
}

function runGame() {
	gameRunning = true;
	if(ttt_game.playersTurn){
		displayStatus("Your turn...", "good");
	}
	else{
		ttt_game.takeAITurn();
	}
}

function stopGame(){
	gameRunning = false;
}



// Enables or disables click events
var gameRunning = false;

// JQuery click events
$(document).ready(function() {
	// AjaxSetup for CSRF token authentication
	// Source: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	            // Send the token to same-origin, relative URLs only.
	            // Send the token only if the method warrants CSRF protection
	            // Using the CSRFToken value acquired earlier
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});	
	$("#tbl-board").on("click", "td", function() {
		if(gameRunning){
			if(ttt_game.playersTurn){
				ttt_game.addUserChoice(event.target.id);
	    		$("#"+event.target.id).addClass("oTaken");
	    	}
	    	else
	    		displayStatus("It's not your turn!", "bad");
		}
	});
	ttt_game = new tictactoe();
	intro();	
	//intro();
});

//CSRF Token authentication below this line
// Source: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
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
