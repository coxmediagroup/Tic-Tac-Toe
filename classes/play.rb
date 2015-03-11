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
    # next_turn(whos_next)
  end
  
  
  def find_best_move
    if @game.find_wins.size > 0
      win = @game.find_wins[0]
      board_slot_target = win[:path][win[:moves].index ""]
      board_slot_target
    elsif @game.find_threats.size > 0
      threats=@game.find_threats
      threat_count = threats.size
      
      # if threat_count == 1
        block = threats[0][:path][threats[0][:moves].index ""]
      # else threat_count > 1
        
      # end
      
      # board_slot_target = win[:path][win[:moves].index ""]
      block
    else
      #if there are no threats we will look for some key positions to take
      open_board
      if @game.get_board.board_array[4]==""
        4
      else
        ##need some sort of algorithm here
        rand_possible_win    
      end
    end
  end
  
  def rand_possible_win
    
  end
  
  def next_turn( who )
    if who == @game.enemy_token
      #give it back to the browser
    else

    end
  end
  
  def game
    @game
  end
  
end