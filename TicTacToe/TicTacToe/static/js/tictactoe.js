var x = "/static/images/x.jpg";
var o = "/static/images/o.jpg";
var blank = "/static/images/blank.jpg";
var o_turn = 0;
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
	$(".tic_slot" ).click(function() {
		id = $(this).attr("id");
		if(values[id]==0){
			values[id]='x';
			o_turn = 1;
			$('#'+id).attr('src',x)
		}	
	});
});


function clean(){
	$(".tic_slot").attr('src',blank)
	for(var key in values){
		values[key]=0;
	}
	o_turn = 0;
    disable = false;
}

