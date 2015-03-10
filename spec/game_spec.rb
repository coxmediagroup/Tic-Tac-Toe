require_relative '../classes/game'
require 'yaml'
require 'spec_helper'

RSpec.describe Game do
  before :each do
    @test_game = Game.new
  end
  
  it 'creates a new Game object with an empty game Board using Game.new' do
    the_board = @test_game.get_board.board_array
    expect( the_board.select{|s| s.include? ""}.size ).to eq the_board.size
  end
  
  it 'will set the board position using apply_move' do
    position_to_set = 5
    token_to_set = "0"
    @test_game.apply_move(position_to_set, token_to_set)
    expect( @test_game.get_board.board_array[position_to_set] ).to eq token_to_set
  end
  
  it 'will return nil instead of applying a move if the position is already taken using apply_move' do
    position_to_set = 5
    token_to_set = "0"
    @test_game.apply_move(position_to_set, token_to_set)
    expect( @test_game.apply_move(position_to_set, "1") ).to eq nil
  end
  
end