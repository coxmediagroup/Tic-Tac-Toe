/**
 * File: libttt.js
 * Author: Kelly Weaver
 *
 * A set of javascript functions to handle our interaction with the tic-tac-toe game
 */

// Returns the state of the board as a 9-character string
function getBoardState()
{
	var str = "---------";
	for (var i = 0; i <= 2; i++)
	{
		var row = $("#row" + i + " .ttt_cell").each(function(k) {
			var index = 3 * i + k;	// index of the current character
			var c = "-";
			if ($(this).hasClass("x_cell"))
				c = "x";
			if ($(this).hasClass("o_cell"))
				c = "o";
			str = str.substr(this, index) + c + str.substr(index + 1);
		});
	}
	return str;
}

// Clears out all css classes and bindings for a cell to remove all interactivity;
// afterwards, you should not be able to click/interact with the cell anymore
function removeInteractivityFromCell(cell)
{
	$(cell).removeClass("null_cell");
	$(cell).removeClass("x_cell");
	$(cell).removeClass("o_cell");
	$(cell).removeClass("hilite_cell");
	$(cell).unbind("click");
	$(cell).unbind("mouseleave");
	$(cell).unbind("mouseenter");
}

// Marks the cell the player selected
function markPlayerCell(cell)
{
	removeInteractivityFromCell(cell);
	$(cell).addClass("x_cell");

	submitMove()
}

// Sends the move to the logic engine, via AJAX
function submitMove()
{
	checkEndState();
	$("#dialog").dialog("open");
	$(".ui-dialog-titlebar-close").hide();
	$.ajax({
		type: "GET",
		url: "http://localhost:8000/gameengine/",
		data: {state: getBoardState() }
	}).done(function(msg) {
		$("#dialog").dialog("close");
		markAICell(msg.charAt(0), msg.charAt(1));
	});
}

// Marks a cell returned from the AI
function markAICell(i, k)
{
	var row = $("#row" + i + " .ttt_cell").each(function(index)
	{
		if (index == k && $(this).hasClass("null_cell"))
		{
			removeInteractivityFromCell($(this));
			$(this).addClass("o_cell");
		}
	});
	checkEndState();
}

// Clears the board for a new game
function clearBoard()
{
	for (var i = 0; i <= 2; i++)
	{
		var row = $("#row" + i + " .ttt_cell").each(function(k) {
			removeInteractivityFromCell($(this));
			bindHoverFunction($(this));
			$(this).addClass("null_cell");
		});
	}
}

function checkColumns()
{
	var board = getBoardState();
	if (board.charAt(0) != '-' && board.charAt(0) == board.charAt(3) && board.charAt(3) == board.charAt(6))
		return board.charAt(0);
	if (board.charAt(1) != '-' && board.charAt(1) == board.charAt(4) && board.charAt(4) == board.charAt(7))
		return board.charAt(1);
	if (board.charAt(2) != '-' && board.charAt(2) == board.charAt(5) && board.charAt(5) == board.charAt(8))
		return board.charAt(2);

	return null;
}

function checkRows()
{
	var board = getBoardState();
	if (board.charAt(0) != '-' && board.charAt(0) == board.charAt(1) && board.charAt(1) == board.charAt(2))
		return board.charAt(0);
	if (board.charAt(3) != '-' && board.charAt(3) == board.charAt(4) && board.charAt(4) == board.charAt(5))
		return board.charAt(3);
	if (board.charAt(6) != '-' && board.charAt(6) == board.charAt(7) && board.charAt(7) == board.charAt(8))
		return board.charAt(6);

	return null;
}

function checkDiagonals()
{
	var board = getBoardState();
	if (board.charAt(0) != '-' && board.charAt(0) == board.charAt(4) && board.charAt(4) == board.charAt(8))
		return board.charAt(0);
	if (board.charAt(2) != '-' && board.charAt(2) == board.charAt(4) && board.charAt(4) == board.charAt(6))
		return board.charAt(2);
	return null;
}

// Checks for a win, lose, or tie
function checkEndState()
{
	var winner = checkColumns();
	if (winner == null)
		winner = checkRows();
	if (winner == null)
		winner = checkDiagonals();
	if (winner == null && getBoardState().indexOf('-') < 0)
		winner = '-';

	if (winner != null)
	{
		var winText = "IT'S A TIE!";
		if (winner == 'x')
			winText = "YOU WIN!";
		if (winner == 'o')
			winText = "I WIN!";

		$("#win_state").dialog("open");
		$("#win_text").html(winText);
	}
}

function bindHoverFunction(cell)
{
	$(cell).hover(function() {
		// Hi-lite the cell, and make it clickable
		$(this).removeClass("null_cell");
		$(this).addClass("hilite_cell");
		$(this).bind("click", function() {
			markPlayerCell(this);
		});
	}, function() {
		// Un-hi-lite the cell, and remove clickability
		$(this).removeClass("hilite_cell");
		$(this).addClass("null_cell");
		$(this).unbind("click");
	});
}

$(document).ready(function() {
	$(".null_cell").each(function() {
		bindHoverFunction($(this));
	});
	$( "#dialog" ).dialog({
		width: 500,
		height: 250,
		modal: true,
		autoOpen: false,
		show: {
			effect: "fade",
			duration: 333
		},
		hide: {
			effect: "puff",
			duration: 333
		}
    });
    $( "#win_state" ).dialog({
			width: 500,
			height: 250,
			modal: true,
			autoOpen: false,
			show: {
				effect: "fade",
				duration: 333
			},
			hide: {
				effect: "puff",
				duration: 333
			}
    });
    $( "button" )
		.button()
		.click(function( event ) {
			event.preventDefault();
			location.href = "/";
	});
});
