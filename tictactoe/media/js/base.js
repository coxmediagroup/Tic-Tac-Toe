var YOUR_MOVE = "post_your_move/";
var CPU_MOVE = "post_cpu_move/";
var BEGIN = "begin/";
var LAST_MOVE = "None"
var LAST_X = "None"
var LAST_Y = "None"


var YOURS_SUCCESS = function(data){
	$( "#dialog" ).dialog("close");
	if(data.error == "1"){
		$( "#dialog" ).html(data.msg);
		$( "#dialog" ).dialog({
			modal: true ,
			open : function(event , ui){
				$(".ui-dialog-titlebar").hide();
			},
			buttons : [
				{
					text : "OK" ,
					click : function(){
						$(this).dialog("close");
						enableBoard();
					}
				}
			],
		});
	}else if(data.won == "1"){
		setBoard(data.board)
		LAST_MOVE = data.last_move;
		LAST_Y = data.last_y;
		LAST_X = data.last_x;
		log("You" , data.time , data.log , data.moves);
		matchWon("You" , data.time);
	}else if(data.draw == "1"){
			setBoard(data.board)
			LAST_MOVE = data.last_move;
			LAST_Y = data.last_y;
			LAST_X = data.last_x;
			log("You" , data.time , data.log , data.moves);
			matchDraw(data.time);
	}else{
		setBoard(data.board)
		LAST_MOVE = data.last_move;
		LAST_Y = data.last_y;
		LAST_X = data.last_x;
		log("You" , data.time , data.log , data.moves);
		$("button#turn").html("cpu");
		doCPUMove()
	}
}

var YOURS_FAIL = function(jqXHR, textStatus){
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",false);
	});
	$( "#dialog" ).html("Error: " + textStatus);
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		}
	});
}

var BEGIN_SUCCESS = function(data){
	$( "#dialog" ).dialog("close");
	if(data.yours){
		$("button#status").html(data.yours);
		setBoard(data.board);
		$("button#turn").html(data.begins);
		log("" , data.time , data.log , data.moves);
		if(data.begins == "cpu"){
			doCPUMove();
		}else{
			enableBoard();
		}
	}
}

var BEGIN_FAIL = function(jqXHR, textStatus){
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",false);
	});
	$( "#dialog" ).html("Error: " + textStatus);
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		}
	});
}

var CPU_SUCCESS = function(data){
	
	$( "#dialog" ).dialog("close");
	if(data.error == "1"){
		$( "#dialog" ).html(data.msg);
		$( "#dialog" ).dialog({
			modal: true ,
			open : function(event , ui){
				$(".ui-dialog-titlebar").hide();
			},
			buttons : [
				{
					text : "OK" ,
					click : function(){
						$(this).dialog("close");
					}
				}
			],
		});
	}else if(data.won == "1"){
			setBoard(data.board)
			LAST_MOVE = data.last_move;
			LAST_Y = data.last_y;
			LAST_X = data.last_x;
			log("CPU" , data.time , data.log , data.moves);
			matchWon("CPU" , data.time);
		}else if(data.draw == "1"){
				setBoard(data.board)
				LAST_MOVE = data.last_move;
				LAST_Y = data.last_y;
				LAST_X = data.last_x;
				log("You" , data.time , data.log , data.moves);
				matchDraw(data.time);
		}else{
		setBoard(data.board)
		LAST_MOVE = data.last_move;
		LAST_Y = data.last_y;
		LAST_X = data.last_x;
		log("CPU" , data.time , data.log , data.moves);
		$("button#turn").html("you");
		enableBoard();
	}
}

var CPU_FAIL = function(jqXHR, textStatus){
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",false);
	});
	$( "#dialog" ).html("Error: " + jqXHR.responseText);
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		}
	});
}

function log(actor , time , log , move){
	if(move == "BEGINS"){
		$("div#log div#data li#begin span").each(function(index , value){
			$(value).removeClass("hide");
			$(value).find("span#time").html(time)
			$(value).find("span#move").html(actor)
			$(value).find("span#log").html(log)
		});
	}else if(move == "ENDS"){
		$("div#log div#data li#end span").each(function(index , value){
			$(value).removeClass("hide");
			$(value).find("span#time").html(time)
			$(value).find("span#move").html(actor)
			$(value).find("span#log").html(log)
		});
		$("div#log div#data li span").each(function(index , value){
			if($(value).hasClass("hide")){
				$(value).parent().css("display" , "none")
			}
		});
	}else{
		m = 9 - move;
		$("div#log div#data li#" + m + " span").each(function(index , value){
			$(value).removeClass("hide");
			$(value).find("span#time").html(time)
			$(value).find("span#move").html(actor)
			$(value).find("span#log").html(log)
		});
	}
}

function matchWon(actor , time){
	log(actor , time , "Won the Match" , "ENDS");
	$( "#dialog" ).html(actor + " Won the Match");
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		},
		buttons : [
			{
				text : "OK" ,
				click : function(){
					$(this).dialog("close");
					initState();
				}
			}
		],
	});
}

function matchDraw(time){
	log("" , time , "Match is Draw" , "ENDS");
	$( "#dialog" ).html("Match is Draw");
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		},
		buttons : [
			{
				text : "OK" ,
				click : function(){
					$(this).dialog("close");
					initState();
				}
			}
		],
	});
}

function enableBoard(){
	$("div#board table tr button , button#status , button#turn").each(function(index , value){
		$(value).prop("disabled",false);
	});
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",true);
	});
	$("button#reset").each(function(index , value){
		$(value).prop("disabled",false);
	});
}

function disableBoard(){
	$("div#board table tr button , button#status , button#turn").each(function(index , value){
		$(value).prop("disabled",true);
	});
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",true);
	});
	$("button#reset").each(function(index , value){
		$(value).prop("disabled",true);
	});
}

function initState(){
	LAST_MOVE = "None"
	LAST_X = "None"
	LAST_Y = "None"
	$("div#board table tr button , button#status , button#turn").each(function(index , value){
		$(value).html("");
		$(value).prop("disabled",true);
	});
	$("div#log div#data li span").each(function(index , value){
		$(value).addClass("hide");
		if($(value).hasClass("hide")){
			$(value).parent().css("display" , "block")
		}
	});
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",false);
	});
	$("button#reset").each(function(index , value){
		$(value).prop("disabled",true);
	});
	$("button#status , button#turn").each(function(index , value){
		$(value).prop("disabled",true);
	});
}

function setBoard(state){
	if(state != null && state.length == 9){
		index = 0;
		for(x = 0 ; x < 3 ; x++){
			for(y = 0 ; y < 3 ; y++){
				if(state[index] == "N"){
					$("div#board table tr button[data-x='"+x+"'][data-y='"+y+"']").html("");
				}else{
					$("div#board table tr button[data-x='"+x+"'][data-y='"+y+"']").html(state[index]);	
				}
				index++;
			}
		}	
	}
}

function getBoard(){
	board = "";
	for(x = 0 ; x < 3 ; x++){
		for(y = 0 ; y < 3 ; y++){
			if($("div#board table tr button[data-x='"+x+"'][data-y='"+y+"']").html() == ""){
				board += "N";
			}else{
				board += $("div#board table tr button[data-x='"+x+"'][data-y='"+y+"']").html();
			}
		}
	}
	return board;
}

function doYourMove(x , y){
	$( "#dialog" ).html("Waiting for Your to Move");
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		}
	});
	disableBoard();
	var request = $.ajax({
	  url: YOUR_MOVE,
	  type: "get",
	  data: {
		"x" : x ,
		"y" : y ,
		"piece" : $("button#status").html() ,
		"board" : getBoard() ,
		"last_move" : LAST_MOVE ,
		"last_x" : LAST_X ,
		"last_y" : LAST_Y ,
	 },
	  dataType: "json"
	});
	request.done(YOURS_SUCCESS);
	request.fail(YOURS_FAIL);
}

function doCPUMove(){
	$( "#dialog" ).html("Waiting for CPU to Move");
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		}
	});
	disableBoard();
	var request = $.ajax({
	  url: CPU_MOVE,
	  type: "get",
	  data: {
		"piece" : $("button#status").html() ,
		"board" : getBoard() ,
		"last_move" : LAST_MOVE ,
		"last_x" : LAST_X ,
		"last_y" : LAST_Y ,
	 },
	  dataType: "json"
	});
	request.done(CPU_SUCCESS);
	request.fail(CPU_FAIL);
}

function beginBoard(){
	initState();
	$("button#begin").each(function(index , value){
		$(value).prop("disabled",true);
	});
	$( "#dialog" ).html("Waiting for Board to be Initialized");
	$( "#dialog" ).dialog({
		modal: true ,
		open : function(event , ui){
			$(".ui-dialog-titlebar").hide();
		}
	});
	var request = $.ajax({
	  url: BEGIN,
	  type: "get",
	  data: {  },
	  dataType: "json"
	});
	request.done(BEGIN_SUCCESS);
	request.fail(BEGIN_FAIL);
}

function resetBoard(){
	alert("reset board");
}

$(document).ready(function(){
	initState();
	$("div#board table tr button").each(function(index , value){
		$(value).click(function(){
			if(!$(this).prop("disabled")){
				doYourMove($(this).data("x") , $(this).data("y"));
			}
		})
	});
	$("button#begin").click(beginBoard);
	$("button#reset").click(initState);
});