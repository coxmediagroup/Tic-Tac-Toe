class Board
  
  @board

  @@corners=[0,2,6,8]
  @@edges=[1,3,5,7]
  @@adjacents = [
    {id: 0, adj: [1,3,4]},
    {id: 1, adj: [0,2,3,4,5]},
    {id: 2, adj: [1,4,5]},
    {id: 3, adj: [0,1,4,6,7]},
    {id: 4, adj: [0,1,2,3,5,6,7,8]},
    {id: 5, adj: [1,2,4,7,8]},
    {id: 6, adj: [3,4,7]},
    {id: 7, adj: [3,4,5,6,8]},
    {id: 8, adj: [4,5,7]}]

  # in your access implementation remember
  # our board is an array, so
  # 0 1 2
  # 3 4 5
  # 6 7 8
  
  def initialize
      @board = ["","","","","","","","",""]
  end
  
  def corners
    @@corners
  end
  
  def edges
    @@edges
  end
  
  def position_open pos=nil
    str_pos = "#{pos}"
    @board[str_pos.to_i]=="" unless str_pos.nil? || str_pos.empty? || str_pos.to_i > @board.length
  end 
  
  def insert_token( pos, token )
    str_pos = "#{pos}"
    @board[str_pos.to_i] = token unless str_pos.nil? || str_pos.empty? || ( token.to_s!="1" && token.to_s!="0")
    @board
  end
  
  def board_array
    @board.dup
  end
  
  def open_positions( positions=[] )
    oc = []
    positions.each do |s|
      if position_open s
        oc << s
      end 
    end
    oc
  end
  
  def most_impacted_open_piece(pieces=[] , token)
    @high_count=0
    @high_corner=nil
    open_positions(pieces).each do |op|
      if adjacent_piece_count(op, token) > @high_count
        @high_count = adjacent_piece_count(op, "0")
        @high_corner = op
      end
    end
    @high_corner
  end  
  
  
  def most_impacted_open_corner(token)
    @high_count=0
    @high_corner=nil
    open_positions( [0,2,6,8]).each do |op|
      if adjacent_piece_count(op, token) > @high_count
        @high_count = adjacent_piece_count(op, "0")
        @high_corner = op
      end
    end
    @high_corner
  end
  
  def adjacent_piece_count(number, token)
    acc = 0
    slots = @@adjacents.find {|x| x[:id] == number}[:adj]
    slots.each do |s|
      acc += @board[s] == token ? 1 : 0
    end
   acc
  end
  
  def corner_adjacent_edge(number)
    if number == 0
      [1,3]
    elsif number == 2
      [1,5]
    elsif number == 6
      [3,7]
    elsif number == 8
      [5,7]
    else
      []
    end
  end
  
  def opposite_edge(number)
    if number == 1 
      7
    elsif number == 3 
      5
    elsif number == 5 
      3
    elsif number == 7 
      1
    end
  end
  
  def opposite_corner(number)
    if number == 8
      0
    elsif number == 0 
      8
    elsif number == 2 
      6
    elsif number == 6 
      2
    else
      nil
    end
  end
  
end