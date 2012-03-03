#
#   Specifications for the Tree class.
#

require 'tree'
require 'state'
require 'state_observer'

module TicTacToe
  describe Tree do

    before(:each) do
      @observe = StateObserver.new
    end

    it "should assemble a tree of successors for a single depth of a given state" do

      @state = State.new [
        1,0,1,
        2,1,2,
        2,1,2
      ]

      Tree.new(@state).generate_successors

      @state.successors.should be_a Hash
      @state.successors.should have(1).item
      @state.successors[1].board.should == [1,1,1,2,1,2,2,1,2]


      @state.board = [
        1,0,1,
        2,1,2,
        2,1,0
      ]
      
      @tree = Tree.new(@state).generate_successors
      # @tree.pretty_print

      @state.successors.should have(2).items
      @state.successors.should be_a Hash

      @state.successors[1].current_player.should == 2
      @state.successors[1].board.should == [1,1,1,2,1,2,2,1,0]
      @observe.terminal?(@state.successors[1]).should be true


      @state.successors[8].current_player.should == 2
      @state.successors[8].board.should == [
        1,0,1,
        2,1,2,
        2,1,1]
      @state.successors[8].successors.should have(0).items
      @observe.terminal?(@state.successors[8]).should be true



      @state.board = [
        1,0,1,
        0,1,2,
        2,1,0
      ]

      Tree.new(@state).generate_successors
      @state.successors.should have(3).items

      @state.successors[1].current_player.should == 2
      @state.successors[1].board.should == [1,1,1,0,1,2,2,1,0]
      @state.successors[1].successors.should have(0).items

    end




    #
    #   work through a slightly more complex one to assert player alternation is functioning properly
    #
    it "should assemble a tree of successors of a given state for a depth of three" do
      @state = State.new [
        0,0,0,
        0,1,2,
        0,0,0
      ]

      Tree.new(@state).generate_successors
      @state.successors.should have(7).items

      @state.current_player.should == 1
      @state.successors[0].board.should == [1,0,0,0,1,2,0,0,0]

      @state.successors[0].current_player.should == 2
      @state.successors[0].successors[2].board.should == [1,0,2,0,1,2,0,0,0]

      @state.successors[0].successors[2].current_player.should == 1
      @state.successors[0].successors[2].successors[1].board.should == [1,1,2,0,1,2,0,0,0]
    end




    it "should iterate over successors for a given state" do
      @state = State.new [
        1,0,2,
        2,1,1,
        2,0,2
      ]

      tree = Tree.new(@state)
      tree.generate_successors

      successors = []
      tree.each_successor do |successor|
        successors << successor
      end
      successors.should have(4).items

      @state = State.new [
        1,0,2,
        2,1,1,
        2,0,0
      ]
      tree = Tree.new(@state)
      tree.generate_successors
      successors = []
      tree.each_successor do |successor|
        successors << successor
      end

      successors.should have(8).items
    end

  end
end