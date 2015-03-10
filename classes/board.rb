class Board
  
  @board
  
  def initialize
      @board = ["","","","","","","","",""]
  end
  def position_open pos=nil
    @board[pos.to_i].empty? unless pos.nil? || pos.empty? || pos.to_i > @board.length
  end 
  
  #returns the board after token is (or maybe is-not) inserted
  def insert_token( pos, token )
    @board[pos.to_i] = token unless pos.nil? || pos.empty? || ( token.to_s!="1" && token.to_s!="0")
    @board
  end
  
  def board_array
    @board.dup
  end
  
  
end