require 'state'

module TicTacToe

  describe State, "initial state is an 9-element zero array" do
    subject { State.new }
    it { should be_empty } # note: we over-ride empty? in State
  end

  describe State, "should track the current player" do
    subject { State.new.current_player }
    it { should == 1 }
  end

  describe State, "should toggle the current player" do
    subject { State.new.toggle_player }
    it { should == 2 }
  end

end

