require_relative '../classes/board'
require 'yaml'
require 'spec_helper'

RSpec.describe Board do
  before :each do   
    @test_board = Board.new
  end
  
  it 'begins with an empty board' do  
    expect(@test_board.board_array).to eq ["","","","","","","","",""]
  end 
  
  it 'returns true for the first bound of an untouched board using position_open()' do
    expect(@test_board.position_open(0)).to eq true
  end
  
  it 'returns nil for out-of-bounds positions using position_open()' do
    expect(@test_board.position_open(10)).to eq nil
  end
  
  it 'accepts position as string using insert_token()' do
    position_to_set = "3"
    token_to_set = "1"
    @test_board.insert_token(position_to_set, token_to_set)
    expect( @test_board.board_array[position_to_set.to_i] ).to eq token_to_set
  end
  
  it 'sets the appropriate bound with a value using insert_token()' do
    position_to_set = 3
    token_to_set = "1"
    @test_board.insert_token(position_to_set, token_to_set)
    expect( @test_board.board_array[position_to_set] ).to eq token_to_set
  end
  
  it 'returns the most current board_array upon completing insert_token()' do
    position_to_set = 3
    token_to_set = "1"
    expect( @test_board.insert_token(position_to_set, token_to_set) ).to eq @test_board.board_array  
  end
end