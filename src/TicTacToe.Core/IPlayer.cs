namespace TicTacToe.Core
{
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
        bool OnTurn(Game state);
    }
}