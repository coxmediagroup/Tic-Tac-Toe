class Board
  
  @board

  # in your access implementation remember
  # our board is an array, so
  # 0 1 2
  # 3 4 5
  # 6 7 8
  
  def initialize
      @board = ["","","","","","","","",""]
  end
  
  def position_open pos=nil
    str_pos = "#{pos}"
    @board[str_pos.to_i].empty? unless str_pos.nil? || str_pos.empty? || str_pos.to_i > @board.length
  end 
  
  #returns the board after token is (or maybe is-not) inserted
  def insert_token( pos, token )
    str_pos = "#{pos}"
    @board[str_pos.to_i] = token unless str_pos.nil? || str_pos.empty? || ( token.to_s!="1" && token.to_s!="0")
    @board
  end
  
  def board_array
    @board.dup
  end
  
  
end