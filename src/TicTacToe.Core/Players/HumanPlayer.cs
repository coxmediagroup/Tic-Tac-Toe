namespace TicTacToe.Core.Players
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
            Name = name;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="IPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        public void OnTurn(Game state)
        {
        }

        public override string ToString()
        {
            return Name;
        }
    }
}