//<script type='text/javascript'>
//<![CDATA[
function getCookie(c_name) {
	var c_value = document.cookie;
	var c_start = c_value.indexOf(" " + c_name + "=");
	if (c_start == -1) {
		c_start = c_value.indexOf(c_name + "=");
	};
	if (c_start == -1) {
		c_value = null;
	} else {
		c_start = c_value.indexOf("=", c_start) + 1;
		var c_end = c_value.indexOf(";", c_start);
		if (c_end == -1) {
			c_end = c_value.length;
		};
		c_value = unescape(c_value.substring(c_start,c_end));
	};
	return c_value;
};

function setCookie(c_name,value,exdays) {
	var exdate=new Date();
	exdate.setDate(exdate.getDate() + exdays);
	var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
	document.cookie=c_name + "=" + c_value;
};

function setCookieFromTextBoxID(c_name) {
	var c_value = "" + document.getElementById(c_name).innerHTML;
	setCookie(c_name,c_value,365)
};

function ReadCookiePref(c_name,c_default) {
	var c_value = getCookie(c_name);
	if (c_value != null && c_value != "") {
	} else {
		setCookie(c_name, c_default, 365);
		c_value = c_default;
	};
	return c_value;
};

function IncrementCookie(c_name) {
	var myvalue = parseInt(ReadCookiePref(c_name,"0"))
	myvalue++;
	setCookie(c_name, myvalue.toString(), 365);
	updateScore();
};

function DecrementCookie(c_name) {
	var myvalue = parseInt(ReadCookiePref(c_name,"0"))
	if (myvalue > 0) {
		myvalue--;
	};
	setCookie(c_name, myvalue.toString(), 365);
	updateScore();
};

function PlayerClickDivSet(c_name, player) {
	if (ReadCookiePref("game_inprogress","no") == "yes") {
		if (ReadCookiePref("whosmove","U") == "U") {
			ClickDivSet(c_name, player);
			setCookie("whosmove","C",365);
			ComputerMove();
		};
	};
};

function ClickDivSet(c_name, player) {
	if (document.getElementById(c_name).innerHTML == "H") {
		document.getElementById(c_name).innerHTML = player;
		document.getElementById(c_name).setAttribute("style","color: #000000;");		
		setCookieFromTextBoxID(c_name);
		if (CheckWins("X")) {
			// Do Player Winner Stuff
			IncrementCookie("wins");
			setCookie("game_inprogress","no",365);
			alert("Player Wins!");
		} else {
			if (CheckWins("O")) {
				// Do Computer Winner Stuff
				IncrementCookie("losses");
				setCookie("game_inprogress","no",365);
				alert("Computer Wins!");
			} else {
				DecrementCookie("movesleft");
				if (MovesLeft() == 0) {
					IncrementCookie("draws");
					setCookie("game_inprogress","no",365);
					alert("No one Wins!");
				};
			};
		};
	};
};

function getRandomInt (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function IsMoveValid(move) {
	if (document.getElementById(move.toString()).innerHTML == "H") {
		return move;
	};
	return 0;
};

function CheckForMove(move, player, aa, bb, cc) {
	var mymove = move;
	if (mymove != 0) {
		return mymove;
	};
	//alert("" + aa.toString() + bb.toString() + cc.toString());
	if ((mymove == 0) && (document.getElementById(aa.toString()).innerHTML == player) && (document.getElementById(bb.toString()).innerHTML == player)) {
		mymove = IsMoveValid(cc);
	};
	if ((mymove == 0) && (document.getElementById(bb.toString()).innerHTML == player) && (document.getElementById(cc.toString()).innerHTML == player)) {
		mymove = IsMoveValid(aa);
	};
	if ((mymove == 0) && (document.getElementById(aa.toString()).innerHTML == player) && (document.getElementById(cc.toString()).innerHTML == player)) {
		mymove = IsMoveValid(bb);
	};
	return mymove;
};

function ComputerMove() {
	var player = "";
	var mypick = 0;
	if (ReadCookiePref("game_inprogress","no") == "yes") {
		if (ReadCookiePref("whosmove","U") == "C") {
			player = "O";
			mypick = CheckForMove(mypick,player,1,2,3);
			mypick = CheckForMove(mypick,player,4,5,6);
			mypick = CheckForMove(mypick,player,7,8,9);
			mypick = CheckForMove(mypick,player,1,4,7);
			mypick = CheckForMove(mypick,player,2,5,8);
			mypick = CheckForMove(mypick,player,3,6,9);
			mypick = CheckForMove(mypick,player,1,5,9);
			mypick = CheckForMove(mypick,player,3,5,7);

			player = "X";
			mypick = CheckForMove(mypick,player,1,2,3);
			mypick = CheckForMove(mypick,player,4,5,6);
			mypick = CheckForMove(mypick,player,7,8,9);
			mypick = CheckForMove(mypick,player,1,4,7);
			mypick = CheckForMove(mypick,player,2,5,8);
			mypick = CheckForMove(mypick,player,3,6,9);
			mypick = CheckForMove(mypick,player,1,5,9);
			mypick = CheckForMove(mypick,player,3,5,7);

			if ((mypick == 0) && (document.getElementById("5").innerHTML == "H")) {
				mypick = IsMoveValid(5);
			};
			if ((mypick == 0) && (document.getElementById("1").innerHTML == "H")) {
				mypick = IsMoveValid(1);
			};
			if ((mypick == 0) && (document.getElementById("3").innerHTML == "H")) {
				mypick = IsMoveValid(3);
			};
			if ((mypick == 0) && (document.getElementById("7").innerHTML == "H")) {
				mypick = IsMoveValid(7);
			};
			if ((mypick == 0) && (document.getElementById("9").innerHTML == "H")) {
				mypick = IsMoveValid(9);
			};
			
			if (mypick == 0) {
				while (mypick == 0) {
					mypick = getRandomInt(1,9);
					if (document.getElementById(mypick.toString()).innerHTML != "H") {
						mypick = 0;
					};
				};
			};
			ClickDivSet(mypick.toString(), "O");
			setCookie("whosmove","U",365);
			//alert("Users move!");
		};
	};
};

function ComputerMoveMake() {
};

function MovesLeft() {
	var ml = 0;
	var a_cnt = 0;
	for (a_cnt = 1; a_cnt < 10; a_cnt++) {
		if (document.getElementById(a_cnt.toString()).innerHTML == "H") {
			ml++;
		};
	};
	return ml;
};

function CheckForWin(player, win, aa, bb, cc) {
	var mywin = false;
	mywin = win;
	if ((document.getElementById(aa.toString()).innerHTML == player) && (document.getElementById(bb.toString()).innerHTML == player) && (document.getElementById(cc.toString()).innerHTML == player)) {
		document.getElementById(aa.toString()).setAttribute("style","background-color: #CC00CC;");
		document.getElementById(bb.toString()).setAttribute("style","background-color: #CC00CC;");
		document.getElementById(cc.toString()).setAttribute("style","background-color: #CC00CC;");
		win = true;
	};
	return win;
};

function CheckWins(player) {
	var win = false;
	// Horizontal Wins
	win = CheckForWin(player, win, 1, 2, 3);
	win = CheckForWin(player, win, 4, 5, 6);
	win = CheckForWin(player, win, 7, 8, 9);
	// Vertical Wins
	win = CheckForWin(player, win, 1, 4, 7);
	win = CheckForWin(player, win, 2, 5, 8);
	win = CheckForWin(player, win, 3, 6, 9);
	// Diagnal
	win = CheckForWin(player, win, 1, 5, 9);
	win = CheckForWin(player, win, 3, 5, 7);
	return win;
};

function updateScore() {
	document.getElementById("score").innerHTML = "Score: " + ReadCookiePref("wins","0") + " Wins / " + ReadCookiePref("losses","0") + " Losses / " + ReadCookiePref("draws","0") + " Draws / " + ReadCookiePref("movesleft","0") + " Moves Left";
};

window.onload = function() {
	//var a_cnt = 0;
	var c_name = "";
	if (ReadCookiePref("game_inprogress","no") != "yes") {
		setCookie("game_inprogress","no",365);
	};
	if (ReadCookiePref("wins","0") == "0") {
		setCookie("wins","0",365);
	};
	if (ReadCookiePref("losses","0") == "0") {
		setCookie("losses","0",365);
	};
	if (ReadCookiePref("draws","0") == "0") {
		setCookie("draws","0",365);
	};
	if (ReadCookiePref("whosmove","") == "") {
		setCookie("whosmove","U",365);
	};
	if ((ReadCookiePref("movesleft","0") == "0") || (ReadCookiePref("movesleft","0") == "9")) {
		setCookie("movesleft","9",365);
		setCookie("whosmove","U",365);
		setCookie("game_inprogress","no",365);
	};

	document.getElementById("reset_board").onclick = function () {
		var c_name = "";
		var mydata = "";
		var a_cnt = 0;
		alert("Let's Play!");
		setCookie("game_inprogress","yes",365);
		setCookie("movesleft","9",365);
		for (a_cnt = 1; a_cnt < 10; a_cnt++) {
			c_name = a_cnt.toString();
			//alert(c_name);
			document.getElementById(c_name).setAttribute("style","color: #444d50;");		
			document.getElementById(c_name).innerHTML = "H";
			document.getElementById(c_name).onclick = (function(c_namea) { return function () { PlayerClickDivSet(c_namea, "X"); }; })(c_name);
			setCookie(c_name,"H",365);
		};
		updateScore()
		setCookie("whosmove","U",365);
		return false;
	};
	for (var a_cnt = 1; a_cnt < 10; a_cnt++) {
		c_name = a_cnt.toString();
		if (ReadCookiePref("game_inprogress","no") == "yes") {
			mydata = ReadCookiePref(c_name, "");
			if (mydata == "H") {
				document.getElementById(c_name).setAttribute("style","color: #444d50; background-color: #444d50;");
			} else {
				document.getElementById(c_name).setAttribute("style","color: #000000; background-color: #444d50;");
			}
			document.getElementById(c_name).innerHTML = mydata;
		};
		document.getElementById(c_name).onclick = (function(c_namea) { return function () { PlayerClickDivSet(c_namea, "X"); }; })(c_name);
	};
	updateScore();
};
//]]>  
//</script>
