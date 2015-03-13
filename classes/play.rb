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
    # whos_next = @token.to_i == 0 ? "1":"0"
    # next_turn(@token.to_i == 0 ? "1":"0")
  end
    
  def game
    @game
  end
  
end