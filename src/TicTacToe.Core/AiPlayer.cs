namespace TicTacToe.Core
{
    using System.Linq;

    using TicTacToe.Core.Actions;

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
        public void OnTurn(Game state)
        {
            // If board is empty, then we're going first, so pick the middle one always
            if (state.Board.IsEmpty())
            {
                var a = new OccupyGameAction(state, this, 1, 1);
				state.PerformAction(a);
            }
        }
    }
}