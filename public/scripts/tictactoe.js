
$(document).ready(function($){
  var jqxhr = $.getJSON( "/new_game", function() {
    // console.log( data );
  });
  
  var board_plays = function(ev){
            var region_mapper = ["nw","n","ne","w","c","e","sw","s","se"];
            var move_made = region_mapper.indexOf(ev.target.id);
            //send an ajax request to our action
            var jqxhr = $.getJSON( "/make_move?move=" + move_made, function() {
            })
              .done(function(data) {
                $.each( data, function(index, item){
                  $.each( item.board , function( index, item ){
                    // console.log( index + " = " + item );
                    switch(item != "" ? index : ''){
                    case 0:
                      $("#nw").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 1:
                      $("#n").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 2:
                      $("#ne").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 3:
                      $("#w").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 4:
                      $("#c").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 5:
                      $("#e").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 6:
                      $("#sw").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 7:
                      $("#s").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    case 8:
                      $("#se").text( item==="0" ? "O" : "X" ).unbind("click");
                      break;
                    default:
                      console.log( "board switched out to default");
                    }
                  });
                  //report the status info
                  if (item.status[0] === "winner"){
                    $("#nw,#n,#ne,#w,#c,#e,#sw,#s,#se").unbind("click");
                    winner_name = item.status[1]==="1" ? "I" : "You";
                    $("#status").text(winner_name + " won!!");
                  }
                  if (item.status[0] === "gameover"){
                    $("#nw,#n,#ne,#w,#c,#e,#sw,#s,#se").unbind("click");
                    $("#status").text("The game is a draw");
                  }
                       
                });
                console.log( "game play was successful" );
              })
              .fail(function() {
                console.log( "game play confirmation error. This is probably a json format error on our side." );
              })
              .always(function() {
                console.log( "ajax transaction to make move has ended" );
              });          
              
          };
  
    $('#nw, #n, #ne, #w, #c, #e, #sw, #s, #se').on('click', board_plays);
    
    $("#reset").click(function(ev){
        var jqxhr = $.getJSON( "/new_game", function() {
        })
          .done(function(data) {
            $.each( data, function(index, item){
              console.log( item.board + ", " + item.status);  
              $("#status").text("");
              $("#nw,#n,#ne,#w,#c,#e,#sw,#s,#se").text("").bind('click',board_plays);                  
            });
            console.log( "game reset was successful" );
          })
          .fail(function() {
            console.log( "game reset confirmation error. This is probably a json format error on our side." );
          })
          .always(function() {
            console.log( "ajax transaction to reset game has ended" );
          });
    });
});

