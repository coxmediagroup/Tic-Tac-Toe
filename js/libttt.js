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
	$.ajax({
		type: "POST",
		url: "http://localhost:8000/gameengine",
		data: {state: getBoardState() }
	}).done(function(msg) {
		alert(msg);
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
});
