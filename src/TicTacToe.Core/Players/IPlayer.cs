namespace TicTacToe.Core.Players
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
        void OnTurn(Game state);
    }
}