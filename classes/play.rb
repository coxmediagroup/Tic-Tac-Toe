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
    #TODO: refactor this mess
    if @game.find_paths_by_status("win").size > 0
      win = @game.find_paths_by_status("win")[0]
      # win = @game.find_wins[0]
      board_slot_target = win[:path][win[:moves].index ""]
      board_slot_target
    elsif @game.find_paths_by_status("threat").size > 0
      threats=@game.find_paths_by_status("threat")
      # threats=@game.find_threats
      threat_count = threats.size
        block = threats[0][:path][threats[0][:moves].index ""]
      block
    else
      #if there are no threats we will look for some key positions to take
      if @game.get_board.board_array[4]==""
        4
      else
        possible_wins = @game.find_paths_by_status("mychance")
        possible_threats = @game.find_paths_by_status("echance") 
        #TODO: kill the opens logic if it's not useful in game debugging 
        opens = @game.find_paths_by_status("none")
        threat_pos=[]
        win_pos=[]
        corners=[0,2,6,8]
        
        possible_wins.each do |pw|
          pw[:moves].each_with_index do |mv, idx|           
            if mv == "" && (win_pos.index( pw[:path][idx]).nil?)
              win_pos << pw[:path][idx]
            end
          end
        end
        # puts "***************** possible wins positions #{win_pos.flatten}"
        
        possible_threats.each do |pt|
          pt[:moves].each_with_index do |emv, idx|           
            if emv == "" && (threat_pos.index(pt[:path][idx]).nil? )
              threat_pos << pt[:path][idx]
            end
          end
        end
        
        opens.each do |op|
          op[:moves].each_with_index do |om, idx|           
            if om == "" && (open_pos.index(op[:path][idx]).nil? )
              open_pos << op[:path][idx]
            end
          end
        end
        
        threat_win_union = threat_pos & win_pos
        available_corners = corners & threat_win_union
        
        if available_corners.size > 0
          available_corners[0]
        else
          if win_pos.size > 0 
            win_pos[0]
          else
            threat_pos[0]
          end
        end
      end
    end
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