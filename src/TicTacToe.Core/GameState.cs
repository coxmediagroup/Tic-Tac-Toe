namespace TicTacToe.Core
{
    using System.Collections.Generic;
    using System.Linq;

    public class GameState
    {
        public Player Player1 { get; internal set; }
        public Player Player2 { get; internal set; }
        public GameBoard Board { get; internal set; }

        /// <summary>
        /// Gets the <see cref="Player"/> who's turn it is.
        /// </summary>
        public Player PlayerTurn { get; internal set; }

        /// <summary>
        /// Create a new <see cref="GameState"/> with 2 players
        /// </summary>
        /// <param name="player1">Player 1</param>
        /// <param name="player2">Player 2</param>
        /// <param name="gameBoard">Game board to use</param>
        public GameState(Player player1, Player player2, GameBoard gameBoard)
        {
            Player1 = player1;
            Player2 = player2;
            Board = gameBoard;
        }
    }

    public class GameBoard
    {
        /// <summary>
        /// Positions and state of the board
        /// </summary>
        public Player[][] BoardPositions { get; internal set; }

        public GameBoard()
        {
            //Create three rows of three board positions
            BoardPositions = Enumerable.Repeat(Enumerable.Repeat<Player>(null, 3).ToArray(),3).ToArray();
        }
    }

    public class Player
    {
        public IAi Ai { get; internal set; }
        public string Name { get; internal set; }

        /// <summary>
        /// Create a human <see cref="Player"/>
        /// </summary>
        /// <param name="name">Name of the human <see cref="Player"/></param>
        public Player(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Create an non human <see cref="IAi"/> <see cref="Player"/>
        /// </summary>
        /// <param name="ai">An <see cref="IAi"/> instance</param>
        public Player(IAi ai)
        {
            Name = ai.Name;
            Ai = ai;
        }
    }

    public interface IAi
    {
        string Name { get; set; }


    }
}
