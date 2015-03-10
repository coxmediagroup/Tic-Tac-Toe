require 'sinatra'
enable :sessions
set :session_secret, '14m45up3r53cr37'

require_relative 'classes/game'
require_relative 'classes/play'

#using gets during initial dev
get '/new_game' do
  @game = Game.new
  session[:game] = @game
  flat_board = @game.get_board.board_array
  # mod_board.select{|s| s.include? ""}.each{ |x| x.replace( "-" )}
  "#{flat_board}"
end

get '/make_move' do
  pos = params[:move].to_s
  game = session[:game]
  @play = Play.new( game: game, move: pos.to_i - 1, token: "0" )
  puts "made a new PLAY object #{@play}"
  session[:game] = @play.game
  board = @play.game.get_board
  "#{board.board_array}"
end