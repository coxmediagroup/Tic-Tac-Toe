require 'board'
require 'player'
require 'computer_player'

module TicTacToe

  describe ComputerPlayer do
    before(:each) do
      @computer_player = ComputerPlayer.new(1)
    end

    it "should score a losing board" do
      @computer_player.score(
        Board.new(
          :matrix => [
            [2,2,2],
            [0,0,0],
            [0,0,0]
          ]
      )).should be -1
    end

    it "should score a winning board" do
      @computer_player.score(
        Board.new(
          :matrix => [
            [1,1,1],
            [0,0,0],
            [0,0,0]
          ]
      )).should be 1
    end


    it "should identify a next move" do

      next_move = @computer_player.next_move(
        Board.new :matrix => [
          [2,0,0],
          [1,2,0],
          [0,1,0]
        ]
      )

      next_move.should == [2,2]

    end

  end

end