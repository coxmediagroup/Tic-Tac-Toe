require_relative 'board'
# require_relative 'play'

class Game
  @@ENEMY_TOKEN="0"
  @@MY_TOKEN="1"
  @board=nil
  @active_token
  @first_offensive_move
  @first_defensive_move
  @last_offensive_move
  @defensive_move_count
  # in your access implementation remember
  # our board is an array, so
  # 0 1 2
  # 3 4 5
  # 6 7 8
  @@debug = false
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
    @defensive_move_count = 0
  end
  
  def active_token
    @active_token
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
  
  
  def game_over( status, player_token )
    
  end
  
  def apply_move( pos, token )
      if @board.position_open(pos)
        @active_token = token
        @board.insert_token(pos, token)
        @first_offensive_move = @first_offensive_move.nil? && token.to_i == 0 ? pos.to_i : @first_offensive_move
        @last_offensive_move = token.to_i == 0 ? pos.to_i : @last_offensive_move
        update_paths
      end
  end
  
  def next_turn( who )
    @active_token = "#{who}"
    if who != enemy_token
      @defensive_move_count += 1
      puts "********************************* making the counter move for #{who}" if @@debug == true
      if @first_defensive_move.nil?
        @first_defensive_move = find_best_move
        puts "*********************** assigning @first_defensive_move : #{@first_defensive_move}" if @@debug == true
        first_play = Play.new( game: self, move: "#{@first_defensive_move}" , token: my_token )
      else
        puts "*********************** already have @first_defensive_move : #{@first_defensive_move}" if @@debug == true
        counter_play = Play.new( game: self, move: "#{find_best_move}" , token: my_token )
      end      
    end
  end
  
  def status
    if( find_paths_by_status("winner").size == 0 && collect_available_moves_from_paths(@game_paths, []).size == 0)
      ["gameover", "-"]
    else
      find_paths_by_status("winner").size > 0 ? ["winner", "#{find_paths_by_status("winner")[0][:moves][0]}"] : ["inplay", "#{@active_token}" ]
    end
  end
  
  def find_paths_by_status( status )
    @game_paths.select{|s| s[:status].include? "#{status}"}
  end
  
  def collect_available_moves_from_paths( path_hashes = [], aggr = [] )
    path_hashes.each do |ph|
      ph[:moves].each_with_index do |mv, idx|           
        if mv == "" && (aggr.index( ph[:path][idx]).nil?)
          aggr << ph[:path][idx]
        end
      end
    end
    aggr
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
        my_damage = p[:moves].count(my_token())
        enemy_damage = p[:moves].count(enemy_token())
        opens = p[:moves].count("")
        if (my_damage==2 && enemy_damage==1) || (my_damage==1 && enemy_damage==2)
          p[:status]="blocked"
        end
        if (my_damage==2 && enemy_damage==0)
          p[:status]="canwin"
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
        if (enemy_damage==3 || my_damage==3)
          p[:status]="winner"
        end
  		end
  	end
    
    puts "*******************************************\n#{@game_paths}\n********************************************" if @@debug == true
  end
   
  def find_best_move
    #TODO: refactor this mess
    if self.find_paths_by_status("canwin").size > 0
      win = self.find_paths_by_status("canwin")[0]
      board_slot_target = win[:path][win[:moves].index ""]
      board_slot_target
    elsif self.find_paths_by_status("threat").size > 0
      threats=self.find_paths_by_status("threat")
      threat_count = threats.size
        block = threats[0][:path][threats[0][:moves].index ""]
      block
    else
        possible_wins = self.find_paths_by_status("mychance")
        possible_threats = self.find_paths_by_status("echance")
        threat_pos = self.collect_available_moves_from_paths( possible_threats, [] )
        win_pos = self.collect_available_moves_from_paths( possible_wins, [] )
        threat_win_union = @first_defensive_move.nil? ? threat_pos : threat_pos || win_pos
        available_corners = @board.corners & threat_win_union
        available_edges = @board.edges & threat_win_union
        
        puts "************************** @board.edges #{@board.edges}" if @@debug == true
        puts "************************** @board.corners #{@board.corners}"  if @@debug == true
        puts "************************** threat_pos #{threat_pos}" if @@debug == true
        puts "************************** win_pos #{win_pos}" if @@debug == true
        puts "************************** threat_win_union #{threat_win_union}" if @@debug == true
        puts "************************** available_corners #{available_corners}" if @@debug == true
        puts "************************** available_edges #{available_edges}" if @@debug == true
        puts "************************** @first_defensive_move #{@first_defensive_move}" if @@debug == true
        puts "************************** @first_offensive_move #{@first_offensive_move}" if @@debug == true
        puts "************************** @last_offensive_move #{@last_offensive_move}" if @@debug == true
        puts "************************** @defensive_move_count #{@defensive_move_count}" if @@debug == true
        
      
        if @first_defensive_move.nil? && @first_offensive_move >= 0
          
          if @board.corners.include? @first_offensive_move 
            if @board.board_array[4] ==""; 4;
            elsif @first_offensive_move == 8; 0;
            elsif @first_offensive_move == 0; 8;
            elsif @first_offensive_move == 2; 6;
            elsif @first_offensive_move == 6; 2;
            end
          elsif @board.edges.include? @first_offensive_move
            if Hash[@board.edges.map.with_index.to_a][@first_offensive_move.to_i]>1 
              available_edges.reverse
            end
            if @board.board_array[4] ==""; 4;
            elsif @first_offensive_move == 1; 7;
            elsif @first_offensive_move == 3; 5;
            elsif @first_offensive_move == 5; 3;
            elsif @first_offensive_move == 7; 1;
            end
          elsif @board.board_array[4].to_i==0
            available_corners[0]
          else
            available_edges[1]            
          end
        else
          #per the pros, if you didn't go first and they take a corner then take the center and take a side adjacent to their last corner play
          if @defensive_move_count == 2 && (@board.corners.include? @last_offensive_move)
            if( 
              (@first_offensive_move == 5 && @last_offensive_move == 0) || 
              ((@first_offensive_move == 1) && (@last_offensive_move == 6 || @last_offensive_move == 8)) || 
              (@first_offensive_move == 3 && @last_offensive_move == 2)
              )
              @board.corner_adjacent_edge(@last_offensive_move)[0]
            elsif (@first_offensive_move == 4 && @last_offensive_move == 8)
              2
            else
              @board.corner_adjacent_edge(@last_offensive_move)[1]
            end
          elsif threat_pos.size > 0
            puts "************************** @last_offensive_move.to_i == 4 => #{@last_offensive_move.to_i == 4}" if @@debug == true
            puts "************************** available_corners.size > 0 => #{available_corners.size > 0}" if @@debug == true
            
            if ((@board.corners.include? @last_offensive_move)|| @last_offensive_move.to_i == 4) && available_corners.length>0
              stupid_choice = ((threat_pos & available_edges).nil? && !threat_pos.nil?) ? threat_pos[0] : (threat_pos & available_corners)[0]
              smarter_choice = @board.most_impacted_open_corner(enemy_token) 
              
              puts "********************** doing the center trap" if @@debug == true
              puts "********************** stupid_choice : #{stupid_choice}" if @@debug == true
              puts "********************** smarter_choice : #{smarter_choice}" if @@debug == true
              
              smarter_choice.nil? ? stupid_choice : smarter_choice
            else
              puts "**********************NOT doing the center trap" if @@debug == true
              puts "**********************@board.most_impacted_open_piece(threat_pos , enemy_token) : #{@board.most_impacted_open_piece(threat_pos , enemy_token)}" if @@debug == true
              puts "**********************@board.most_impacted_open_corner(enemy_token) : #{@board.most_impacted_open_corner(enemy_token)}" if @@debug == true
              (@board.most_impacted_open_piece(threat_pos , enemy_token) != 4) && !@board.most_impacted_open_corner(enemy_token).nil? ? @board.most_impacted_open_corner(enemy_token) : @board.most_impacted_open_piece(threat_pos , enemy_token)
            end
          elsif win_pos.size > 0 
            if @board.corners.include? @last_offensive_move
              if available_corners.size > 0 
                 available_corners[0] 
               else 
                 threat_win_union[0]
               end
            else
              available_edges.size > 0 ? available_edges[0] : threat_win_union[0]
            end
          else
            threat_pos[0]
          end
        end
    end
  end #end find_best_move
   
end