var x = "/static/images/x.jpg";
var o = "/static/images/o.jpg";
var blank = "/static/images/blank.jpg";
var o_turn = 0;
var disable = false
var values = {
	"A":0,
	"B":0,
	"C":0,
	"D":0,
	"E":0,
	"F":0,
	"G":0,
	"H":0,
	"I":0,
}

$(document).ready(function() {
	first_move = $('#first_move').attr("value");
	values[first_move]='o';	
	$("#"+first_move).attr('src',o)
	$(".tic_slot" ).click(function() {
		id = $(this).attr("id");
		if(values[id]==0 && !disable){
			if(!o_turn){
				values[id]='x';
				o_turn = 1;
				$('#'+id).attr('src',x)
				send_ajax();
			}
			
		}	
	});
});
	
function send_ajax(){
	var info = [];
	for(var key in values){
		info.push(values[key]);
	}
	$.ajax({
			url : "/send_state_ajax",
			type : "POST",
			dataType: "json",
			data : {
				'info':info,
			},
		success : function(json) {
				$('#'+json.next_move).attr('src',o)
				values[json.next_move]='o'
				o_turn = 0
				if(json.win=='true'){
					disable = true;
					alert("I won")
				}
		},
		error : function(xhr,errmsg,err) {
				alert(xhr.responseText);
		}
	});
}
function clean(){
	$(".tic_slot").attr('src',blank)
	for(var key in values){
		values[key]=0;
	}
	$.ajax({
			url : "/first_move_json",
			type : "POST",
			dataType: "json",
			data : {
			},
		success : function(json) {
				first_move = json.first_move;
				values[first_move]='o';	
				$("#"+first_move).attr('src',o)
		},
		error : function(xhr,errmsg,err) {
				alert(xhr.responseText);
		}
	});
	o_turn = 0;
    disable = false;

	
}
