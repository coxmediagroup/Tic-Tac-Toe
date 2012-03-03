#
#   Specifications for the StateObserver class.
#
module TicTacToe
  class StateObserver

    def terminal?(state); filled?(state) or won?(state); end
    def draw?(state); filled?(state) and winner(state) == 0; end

    def won?(state); winner(state) != 0; end
    def player_won?(state, n); winner(state) == n; end
    def first_player_won?(state, n); player_won?(state, 1); end

    def open_positions(state)
      open = []
      state.board.each_with_index { |c, i| open << i if c == 0 }
      open
    end

    def winner(state)
      win_player = 0
      each_line(state) do |line|
        if line.first != 0 and line.uniq.length == 1
          win_player = line.first
          break
        end
      end
      win_player
    end

    def evaluate(state, player)
      return 0 if draw?(state)
      player_won?(state, player) ? 1 : -1
    end

    def filled?(state)
      state.board.each do |value|
        return false if value == 0
      end
      true
    end

    def pretty_print(state,value_map=[' ','X','O'])
      puts pretty(state,value_map)
    end
    
    def pretty(state,value_map=[' ','X','O'])
      txt = StringIO.new

      m = matrix(state)
      m.each_with_index do |row, n|
        txt << row.map do |value|
          mark = value_map[value]
          line = " #{mark} "
          line
        end.join('|') << "\n"

        # draw a line between each row
        txt << "-"*((3*3)+(2)) << "\n" unless n == 2
      end

      txt.rewind
      txt.read
    end

    private

    def matrix(state)
      f = state.board
      [[f[0], f[1], f[2]],
       [f[3], f[4], f[5]],
       [f[6], f[7], f[8]]]
    end

    def diagonals(state)
      m = matrix(state)

      [ (0..2).collect { |i| m[i][i] },
        (0..2).collect { |i| m[i][2-i] } ]
    end

    def each_line(state)
      m = matrix(state)
      
      lines = (m + m.transpose + diagonals(state))

      lines.each do |line|
        yield line
      end
    end
  end
end