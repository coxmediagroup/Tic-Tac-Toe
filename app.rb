require 'sinatra'
enable :sessions
set :session_secret, '14m45up3r53cr37'

require_relative 'classes/game'
require_relative 'classes/play'

#using gets during initial dev
get '/tic-tac-toe' do
  erb :index
end

get '/follower_viz' do
  @user = params[:user]
  erb :follower
end
 
get '/repo_viz' do
  @user = params[:user]
  erb :repo
end

get '/new_game' do
  @game = Game.new
  session[:game] = @game
  "[{\"board\": #{@game.get_board.board_array}, \"status\": [\"new\",\"0\"]}]"
end

get '/make_move' do
  pos = params[:move].to_i.between?(0,8) ? params[:move].to_s : ""
  game = session[:game]
  #accept client play
  @play = Play.new( game: game, move: pos , token: game.enemy_token )
  #make AI play
  @play.game.status[0] == "winner" || @play.game.status[0] == "gameover" ? @play.game.game_over(@play.game.status[0], @play.game.status[1]) : @play.game.next_turn(@play.game.active_token.to_i == 0 ? "1":"0")
  session[:game] = @play.game
  board = @play.game.get_board
  "[{\"board\": #{board.board_array},\"status\": #{@play.game.status}}]"
end
  
  
  
# mod_board.select{|s| s.include? ""}.each{ |x| x.replace( "-" )}
__END__
 
@@ index
<html>
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>TTT</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function($){
      var jqxhr = $.getJSON( "/new_game", function() {
        // console.log( data );
      });
      
      var board_plays = function(ev){
                var region_mapper = ["nw","n","ne","w","c","e","sw","s","se"];
                var move_made = region_mapper.indexOf(ev.target.id);
                //send an ajax request to our action
                var jqxhr = $.getJSON( "/make_move?move=" + move_made, function() {
                  // console.log( data );
                })
                  .done(function(data) {
                    // console.debug(data);
                    $.each( data, function(index, item){
                      // console.log( item.board + ", " + item.status);
                      //fill the board
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
              // console.log( data );
            })
              .done(function(data) {
                // console.debug(data);
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
    
    </script>
  </head>
  <body>
    <style>
    h1 {
      text-align: center;
    }
    
    .container {
      position: relative;
      width: 500px;
      height: 500px;
      margin: auto;
      background-color: #E2E2E2;
    }
    
    table {
      background-color: #A3B1BD;
      margin: auto;
    }
    
    td {
      height:50px;
      width:50px; 
    }
    
    span {
      padding: 0px; 
      background-color: #E7EBF0;
      font-size: 3em;
      height:100px;
      line-height: 100px;
      width:100px;
      text-align: center;
      vertical-align: middle;
    }
    
    #status {
      display: block;
      color: blue;
      background-color: white; 
      text-align: center;
      margin: auto;
      width: 100% ;
    }
    
    #reset {
      display: block;
      background-color: #728497;
      color: white;
      padding: 5px;
      width: 100px;
      height: 19px;
      line-height: 19px;
      font-size: 1em;
      margin: auto;
    }
    
    #reset:hover {
      background-color: #727272;
    }
    
    span:hover  {
      background-color: #D4D4D4;
    }
    
    #nw {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #n {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #ne {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #w {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #c {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #e {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #sw  {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #s  {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    #se  {
      display: block;
      border-right: 2px solid black;
      border-bottom:  2px solid black;
    }
    
    </style>
    <div class="container">
      <h1>Tic Tac Toe</h1>
      <div class="board">
        <table>
          <thead/>
          <tbody>
            <tr>
              <td><span id="nw"></span></td>
              <td><span id="n"></span></td>
              <td><span id="ne"></span></td>
            </tr><tr>
              <td><span id="w"></span></td>
              <td><span id="c"></span></td>
              <td><span id="e"></span></td>
            </tr><tr>
              <td><span id="sw"></span></td>
              <td><span id="s"></span></td>
              <td><span id="se"></span></td>
            </tr>
          </tbody>
        </table>
        <p>
          <span id="reset">Reset the game</span>
        </p>
        <p>
          <span id="status"></span>
        </p>
      </div>
    </div>
  </body>
</html>
 
@@ follower
<p>here comes the crazy follower_viz for <%= @user %></p>
 
@@ repo
<h1>this viz from <%= @user %>'s repos is HUGE!</h1>