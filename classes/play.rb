require_relative 'board'

class Play
  @position
  @token
  @board
  @game
  
  def initialize params 
    @position = "#{params[:move]}"
    @token = "#{params[:token]}"
    @game = params[:game]
    @board = @game.get_board
    commit
  end
  
  def game
    @game
  end
  
  def commit
    unless @position.nil? || @position.empty? || @token.nil? || @token.empty? 
      if @board.position_open(@position)
        @board.insert_token(@position,@token)
      end
    end
  end
  
end