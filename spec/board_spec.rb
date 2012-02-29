#
#
#    Specifications for the TicTacToe::Board class.
#
#
require 'board'

module TicTacToe

  describe Board, "constructor interface" do
    it "may be constructed without options" do
      @board = Board.new

      # should have sane defaults
      @board.size.should == [3,3]
    end

    it "may be constructed with optional :size parameter" do
      @board = Board.new :size => [4,4]
      @board.matrix.length.should    be 4
      @board.matrix[0].length.should be 4
    end
  end

  #
  #  A board should be able to manage inscriptions and construct
  #  a plaintext representation of the current game state.
  #
  describe Board, "inscription handling" do
    before(:each) do
      @board = Board.new
    end

    it "should accept inscriptions" do
      
      @board.inscribe! 1, [0, 0]
      @board.at(0,0).should be 1


      @board.inscribe! 2, [2,1]
      @board.at(2,1).should be 2
    end

    it "should format an empty board for display" do
      @board.pretty.should == "   |   |   \n-----------\n   |   |   \n-----------\n   |   |   \n"
    end

    it "should format an inscribed board for display" do
      # make a few marks
      @board.inscribe! 1, [0,1]
      @board.inscribe! 2, [1,2]
      @board.pretty.should == "   | X |   \n-----------\n   |   | O \n-----------\n   |   |   \n"
    end
  end
  

  describe Board, "game analysis" do
    it "should gather legal moves" do
      @board = Board.new(:matrix => [
        [0,2,1],
        [1,1,2],
        [2,2,0]
      ]).unmarked_positions.should == [[0,0],[2,2]]
    end
    
  end


  #
  #  A board should be able to detect various end-game conditions.
  #
  describe Board, "end game detection" do

    it "should detect a draw" do
      @board = Board.new :matrix => [
        [2,2,1],
        [1,1,2],
        [2,2,1]
      ]

      @board.winner.should be nil
    end

    it "should detect a horizontal win" do
      @board = Board.new :matrix => [
        [2,2,1],
        [1,1,1],
        [1,2,2]
      ]

      @board.winner.should be 1
    end

    it "should detect a diagonal win" do
      @board = Board.new :matrix => [
        [2,2,1],
        [2,1,2],
        [1,2,2]
      ]

      @board.winner.should be 1
    end

  end
end