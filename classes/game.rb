require_relative 'board'
require_relative 'play'

class Game
  @@ENEMY_TOKEN="0"
  @@MY_TOKEN="1"
  @board=nil
  @remote_threats=0
  @immediate_threats=0
  @immediate_wins=0
  
  # in your access implementation remember
  # our board is an array, so
  # 0 1 2
  # 3 4 5
  # 6 7 8
  
  @game_paths = []
  
  def initialize
    @board = Board.new
    @game_paths = [
    {id: 1, path: [0,1,2], moves: ["","",""], status: "open"},
    {id: 2, path: [3,4,5], moves: ["","",""], status: "open"},
    {id: 3, path: [6,7,8], moves: ["","",""], status: "open"},
    {id: 4, path: [0,3,6], moves: ["","",""], status: "open"},
    {id: 5, path: [1,4,7], moves: ["","",""], status: "open"},
    {id: 6, path: [2,5,8], moves: ["","",""], status: "open"},
    {id: 7, path: [0,4,8], moves: ["","",""], status: "open"},
    {id: 8, path: [2,4,6], moves: ["","",""], status: "open"}
    ]

  end
  
  def enemy_token
    @@ENEMY_TOKEN
  end
  
  def my_token
    @@MY_TOKEN
  end
  
  def get_board
    bd = @board
    bd
  end
  
  def apply_move( pos, token )
      if @board.position_open(pos)
        @board.insert_token(pos, token)
        update_paths
      end
  end
  
  # def find_threats
  #   @game_paths.select{|s| s[:status].include? "threat"}
  # end
  #
  # def find_wins
  #  wins = @game_paths.select{|s| s[:status].include? "win"}
  #  wins
  # end
  #
  # def find_possible_wins
  #   pwins = @game_paths.select{|s| s[:status].include? "mychance"}
  #   pwins
  # end
  #
  # def find_possible_wins
  #   epwins = @game_paths.select{|s| s[:status].include? "enemychance"}
  #   epwins
  # end
  
  def find_paths_by_status( status )
    @game_paths.select{|s| s[:status].include? "#{status}"}
  end
  
  def update_paths
  	@board.board_array.each.with_index do |piece, idx|
  		@game_paths.each do |p|
  			#blanket fill in of the board from message in
  			hit_pos = Hash[p[:path].map.with_index.to_a][idx]
        if !hit_pos.nil?
    			p[:moves][hit_pos]="#{piece}"
        end
        #evaluate the moves for a status
        my_damage = p[:moves].count(@@MY_TOKEN)
        enemy_damage = p[:moves].count(@@ENEMY_TOKEN)
        opens = p[:moves].count("")
        if (my_damage==2 && enemy_damage==1) || (my_damage==1 && enemy_damage==2)
          p[:status]="blocked"
        end
        if (my_damage==2 && enemy_damage==0)
          p[:status]="win"
        end
        if (enemy_damage==2 && my_damage==0)
          p[:status]="threat"
        end
        if (my_damage==1 && opens==2)
          p[:status]="mychance"
        end
        if (enemy_damage==1 && opens==2)
          p[:status]="echance"
        end
  		end
  	end
    
    #TODO: remove this after the debugging is done
    # puts "#{@game_paths}"
  	#rat out the "O"s
  end
   
end