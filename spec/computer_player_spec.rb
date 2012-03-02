require 'board'
require 'player'
require 'computer_player'
require 'maximizing_player'

module TicTacToe

  describe ComputerPlayer, "minimax implementation" do
    before(:each) do
      @player = MaximizingPlayer.new
    end



    it "should evaluate a win, loss and draw" do
      @player.evaluate(Board.new :field => [
        1,1,1,
        1,2,1,
        2,1,2
      ]).should == 1

      @player.evaluate(Board.new :field => [
        1,1,2,
        1,2,1,
        2,1,2
      ]).should == -1

      @player.evaluate(Board.new :field => [
        1,2,1,
        1,2,1,
        2,1,2
      ]).should == 0
    end

    it "should rank two moves at a single depth relative to one another (endgame)" do
      @board = Board.new :field => [
        2,0,1,
        2,2,0,
        1,2,1
      ]
      @player.move(@board).should == [1,2]
    end

    it "should rank three moves relative to one another (next-to-engame)" do
      @board = Board.new :field => [
        1,0,2,
        2,2,0,
        1,0,1
      ]
      @player.move(@board).should == [2,1]
    end

    it "should rank four moves relative to one another (slightly more than halftime)" do
      @board = Board.new :field => [
        1,0,0,
        2,2,0,
        1,0,1
      ]
      @player.move(@board).should == [2,1]
    end


    # something funny here?
    it "should identify an 'early' winning move" do

      @board = Board.new :field => [
        1,2,0,
        2,0,0,
        0,0,1
      ] # of course very unlikely (but possible) that this could arise

      @player.move(@board).should == [1,1]
    end

    it "should defend against an 'early' attack" do
      @board = Board.new :field => [
        1,0,2,
        0,0,0,
        0,0,2
      ]
      @player.move(@board).should == [1,2]
    end
=begin

    it "should play on a corner for the first move" do
      @board = Board.new
      @player.next_move(@board).should == [0,0]
    end
=end
=begin


    it "should identify a necessary countermove" do

      @player.number = 2
      @board = Board.new :turn => 2, :field => [
        0,2,0,
        0,2,0,
        1,1,0
      ]

      puts @board.pretty
      move = @player.next_move(@board)
      move.should == [2,2]

    end
=end
    #
    #   run through legal opening moves -- should play them to a win or draw
    #
#    it "should play optimally" do
#      @board = Board.new
#      @opponent = ComputerPlayer.new(2)
#
#      opening_moves = @board.legal_next_states(2)
#      puts "--- Examining list of openings: #{opening_moves}"
#
#      opening_moves.each do |board|
#
#        puts "--- playing against board: "
#        puts
#        puts board.pretty
#
#        # puts "--- allowing opponent to move first..."
#        # @opponent.move(board)
#
#        until board.done?
#          #puts @board.pretty
#          #puts
#          @player.move(board)
#          @opponent.move(board) unless board.done?
#        end
#
#        won_or_draw = board.winner == nil or board.winner == @player.number
#        won_or_draw.should == true
#      end
#    end
    
  end # end describe ComputerPlayer
end