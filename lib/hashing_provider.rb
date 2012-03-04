#
# ///
module TicTacToe
  #
  #  Provide hashing services for various purposes. For now really just
  #  for the transposition table (also in progress) but eventually we could
  #  use a zorbist to represent the game board itself, and XOR as needed;
  #  WAY cheaper than the current method obviously
  #
  module HashingProvider
    #
    #  get a unique hash per board configuration / player
    #
    def hash(state)
      key = state.current_player.to_s + state.board.hash.to_s
      key.to_i
    end
  end
end