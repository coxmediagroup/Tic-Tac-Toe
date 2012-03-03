#
#
#
#  zobrist hash and transposition -- under construction
#
#  notes:
#     - i actually attempted to integrate this but the result was REALLY slow,
#     probably because of manually calculating all those stupid matrix reversals
#     and transpositions in ruby. refactoring the board to use bitset, and hard-coding
#     the transformations might do the trick.
#     
#
module TicTacToe
  class Zobrist

    #
    #   use zobrist to get a unique hash per board configuration
    #
    def Zobrist.hash(matrix)

      # should seed...
      r ||= Array.new(3) { |i| Array.new(3) { |j| Array.new(3) { |k| rand } } }

      key = 0
       matrix.each_with_index do |row, x|
        row.each_with_index do |value, y|
          key ^= r[x][y][value]
        end
      end
      key
    end
#
#    e.g.:
#
#    def Minimax._zobrist_value(state, player=1, depth=0, observe=StateObserver.new)
#
#      @@transpositions ||= {}
#
#      matrix             = observe.matrix(state)
#      transpose          = observe.transpose(state)
#      inverse            = observe.flip_vertical(state)
#      inverse_horizontal = observe.flip_horizontal(state)
#      rotated            = observe.rotate(state)
#      rotated_ccw        = observe.rotate_ccw(state)
#      transpositions     = [ matrix, transpose, inverse,
#                             inverse_horizontal, rotated, rotated_ccw ]
#
#      val = nil
#      state_hashes = transpositions.map { |t| Minimax.hash(t,player) }
#      state_hashes.each do |state_hash|
#        val = @@transpositions[state_hash] if @@transpositions.has_key? state_hash
#      end
#
#      val = _value(state, player, depth, observe)
#
#      state_hashes.each do |state_hash|
#
#        @@transpositions[state_hash] = val
#
#      end
#
#      val
#    end
  end
end