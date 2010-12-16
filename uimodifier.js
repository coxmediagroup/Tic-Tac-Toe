/*This file is intended to help clean up anything dealing with UI and to improve the user experience*/

/* Why are we doing this? Because we need to attach a function later 
 * on to disallow selection
 * across multiple browsers including IE6. */ 
function returnFalse()  
{
	return false;
}

/* Er, um, what?!?!? This is a quick way to check if we're using IE.
 * Why? Well, the statement following this would throw up an error if we were using
 * some sort of legit browser like Chrome, Firefox, or Safari.
 * I can't take credit for this, as I found this diddy at http://tinyurl.com/ldmzrg */
var IE = /*@cc_on!@*/false;

/*And here's where we disable selection for IE browsers.*/
if (IE) {
	window.onload = function() {
		document.getElementById('board').attachEvent('onselectstart', returnFalse);
	}
}

/*This let's us know a cell has been clicked. So, er, um, yeah, it means do something!*/


$(document).ready(function() {
    $("#board td").click(function(e) {
        alert($(this).parent().index() + " " + $(this).parent().children().index($(this)));
    });
});
