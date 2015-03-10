require_relative 'board'
require_relative 'play'

class Game
  
  @board=nil
  @remote_threats=0
  @immediate_threats=0
  @immediate_wins=0
  
  @game_paths = [
  {id: 1, path: [1,2,3], moves: ["","",""], status: "open"},
  {id: 2, path: [4,5,6], moves: ["","",""], status: "open"},
  {id: 3, path: [7,8,9], moves: ["","",""], status: "open"},
  {id: 4, path: [1,4,7], moves: ["","",""], status: "open"},
  {id: 5, path: [2,5,8], moves: ["","",""], status: "open"},
  {id: 6, path: [3,6,9], moves: ["","",""], status: "open"},
  {id: 7, path: [1,5,9], moves: ["","",""], status: "open"},
  {id: 8, path: [3,5,7], moves: ["","",""], status: "open"}
  ]
  
  def initialize
    @board = Board.new
  end
  
  def get_board
    bd = @board
    bd
  end
  
  def apply_move( pos, token )
    # unless pos.nil? || pos.empty? || token.nil? || token.empty?
      if @board.position_open(pos)
        @board.insert_token(pos, token)
      end
    # end
  end
   
end