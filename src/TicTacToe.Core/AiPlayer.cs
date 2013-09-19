namespace TicTacToe.Core
{
    public class AiPlayer : IPlayer
    {
        public string Name { get; private set; }

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
        /// <returns>True to end the turn, False otherwise. Human players would return False, while AI would return True.</returns>
        public bool OnTurn(Game state)
        {
            return true;
        }
    }
}