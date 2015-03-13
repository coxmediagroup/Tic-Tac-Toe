require 'sinatra'
enable :sessions
set :session_secret, '14m45up3r53cr37'

require_relative 'classes/game'
require_relative 'classes/play'

#using gets during initial dev
get '/tic-tac-toe' do
  erb :index
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

__END__
 
@@ index
<html>
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>TTT</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    <script type="text/javascript" src="scripts/tictactoe.js"></script>
    <link rel="stylesheet" type="text/css" href="css/tictactoe.css"/>
    <link >
    <script type="text/javascript"></script>
  </head>
  <body>
    <style></style>
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