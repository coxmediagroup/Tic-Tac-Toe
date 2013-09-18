namespace TicTacToe.Core
{
    public class HumanPlayer : IPlayer
    {
        public string Name { get; internal set; }

        /// <summary>
        /// Create a <see cref="HumanPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="HumanPlayer"/></param>
        public HumanPlayer(string name)
        {
            this.Name = name;
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

        public override string ToString()
        {
            return this.Name;
        }
    }
}