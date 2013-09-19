namespace TicTacToe.Core
{
    using System.Collections.Generic;
    using System.Linq;

    using TicTacToe.Core.Actions;

    public class AiPlayer : IPlayer
    {
        public string Name { get; internal set; }

        /// <summary>
        /// Create a <see cref="AiPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="AiPlayer"/></param>
        public AiPlayer(string name)
        {
            this.Name = name;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="AiPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        public void OnTurn(Game state)
        {
            // If board is empty, then we're going first, so pick the middle one always
            if (state.Board.IsEmpty())
            {
                var a = new OccupyGameAction(state, this, 1, 1);
				state.PerformAction(a);
                return;
            }

			// Otherwise, things get a bit sticky here.
			// I suppose we can brute force this sucker and see
			//    how long it takes first.

            var result = new PlayItOutResults(this, state.Board, state);
        }

        public override string ToString()
        {
            return Name;
        }

        internal class PlayItOutResults
        {
			public int Index { get; internal set; }
            public List<PlayItOutResults> Moves { get; internal set; }
			public GameWinStatus Status { get; internal set; }
			public IPlayer WinPlayer { get; internal set; }
			public Game Game { get; set; }

            public PlayItOutResults(IPlayer movePlayer, GameBoard board, Game game)
            {
                Game = game;
                Index = -1;
                Moves = new List<PlayItOutResults>();
                for (var i = 0; i < 9; i++)
                {
                    if (!board.IsPositionOccupied(i))
                    {
                        var res = new PlayItOutResults(i, movePlayer, board, game);
						Moves.Add(res);
                    }
                }
            }

            public PlayItOutResults(int idx, IPlayer movePlayer, GameBoard board, Game game)
            {
                Game = game;
                Moves = new List<PlayItOutResults>();
                Index = idx;
                var bclone = CloneBoard(board);
                bclone.Occupy(movePlayer, idx);

				//Check if it's a win
                WinPlayer = bclone.Winner();
                if (WinPlayer != null)
                {
                    Status = GameWinStatus.Win;
                    return;
                }

				// Check if it's a tie
                if (bclone.IsFull())
                {
                    Status = GameWinStatus.Tie;
                    return;
                }

                // invert move player
                var newMovePlayer = movePlayer == Game.Player1 ? Game.Player2 : Game.Player1;

                for (var i = 0; i < 9; i++)
                {
                    if (!bclone.IsPositionOccupied(i))
                    {
                        var res = new PlayItOutResults(i, newMovePlayer, bclone, Game);
                        Moves.Add(res);
                    }
                }
            }

            internal GameBoard CloneBoard(GameBoard board)
            {
                var bclone = new GameBoard();
                for (var row = 0; row < board.BoardPositions.Length; row++)
                {
                    for (var p = 0; p < board.BoardPositions[row].Length; p++)
                    {
                        bclone.BoardPositions[row][p] = board.BoardPositions[row][p];
                    }
                }
                return bclone;
            }
        }
    }
}