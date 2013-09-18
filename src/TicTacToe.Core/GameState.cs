namespace TicTacToe.Core
{
    using System.Collections.Generic;
    using System.Linq;

    public class GameState
    {
        public IPlayer Player1 { get; internal set; }
        public IPlayer Player2 { get; internal set; }
        public GameBoard Board { get; internal set; }

        /// <summary>
        /// Gets the <see cref="Player"/> who's turn it is.
        /// </summary>
        public IPlayer PlayerTurn { get; internal set; }

        /// <summary>
        /// Create a new <see cref="GameState"/> with 2 players
        /// </summary>
        /// <param name="player1">Player 1</param>
        /// <param name="player2">Player 2</param>
        /// <param name="gameBoard">Game board to use</param>
        public GameState(IPlayer player1, IPlayer player2, GameBoard gameBoard)
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
        public IPlayer[][] BoardPositions { get; internal set; }

        public GameBoard()
        {
            //Create three rows of three board positions
            BoardPositions = Enumerable.Repeat(Enumerable.Repeat<IPlayer>(null, 3).ToArray(), 3).ToArray();
        }
    }

    public class HumanPlayer : IPlayer
    {
        public string Name { get; internal set; }

        /// <summary>
        /// Create a <see cref="HumanPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="HumanPlayer"/></param>
        public HumanPlayer(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="IPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        /// <returns>True to end the turn, False otherwise. Human players would return False, while AI would return True.</returns>
        public bool OnTurn(GameState state)
        {
            return false;
        }
    }

    public interface IPlayer
    {
        /// <summary>
        /// Name of the <cref see="IPlayer"/>
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Gets invoked when it's the <cref see="IPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        /// <returns>True to end the turn, False otherwise. Human players would return False, while AI would return True.</returns>
        bool OnTurn(GameState state);
    }
}
