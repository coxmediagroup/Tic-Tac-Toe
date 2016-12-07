require_relative 'board'
require_relative 'game'


class Play
  @position
  @token
  @board
  @game
  
  def initialize params 
    @position = "#{params[:move]}"
    @token = "#{params[:token]}"
    @game = params[:game]
    @game.apply_move(@position, @token)
  end
    
  def game
    @game
  end
  
end