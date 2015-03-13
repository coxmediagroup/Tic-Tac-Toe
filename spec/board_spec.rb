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
  
  it 'returns a count of specific adjacent pieces using adjacent_piece_count( space, piece )' do
    @test_board.insert_token(0, "0")
    @test_board.insert_token(5, "0")
    @test_board.insert_token(7, "0")
    
    expect( @test_board.adjacent_piece_count( 8, "0") ).to eq 2
  end

  it 'returns the most vulnerable open corner using most_impacted_open_corner()' do
    @test_board.insert_token(0, "0")
    @test_board.insert_token(5, "0")
    @test_board.insert_token(7, "0")
    
    expect( @test_board.most_impacted_open_corner("0") ).to eq 8
  end

  it 'returns the most vulnerable open corner using most_impacted_open_piece(pieces=[] , token)' do
    @test_board.insert_token(0, "0")
    @test_board.insert_token(5, "0")
    @test_board.insert_token(7, "0")
    
    expect( @test_board.most_impacted_open_piece([0,1,2,3,4,5,6,7,8] , "0") ).to eq 4
  end
  #open_positions( positions=[] )
  
  it 'returns an array of the open positions from the array passed in using open_positions( positions[] )' do
    @test_board.insert_token(0, "0")
    @test_board.insert_token(5, "0")
    @test_board.insert_token(7, "0")
    
    expect( @test_board.open_positions([0,1,2,3,4,5,6,7,8]) ).to eq [1,2,3,4,6,8]
  end
end