using System.Linq;
using System.Management.Instrumentation;
using System.Reflection;
using Common.Logging;
using TicTacToe.Core.Actions;
using TicTacToe.Core.Players.AI;
using TicTacToe.Core.Utils;

namespace TicTacToe.Core.Players
{
    public class AiPlayer : IPlayer
    {
        internal static ILog Log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);
        public string Name { get; internal set; }
		public int TurnDelay { get; set; }
		public bool IsLearning { get; set; }

        /// <summary>
        /// Create a <see cref="AiPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="AiPlayer"/></param>
        /// <param name="focus">Choose what the Ai is more focused on achieving</param>
        /// <param name="turnDelay">Time to wait before switching the turn in ms(Default: 0)</param>
        public AiPlayer(string name, bool isLearning, int turnDelay = 0)
        {
            this.Name = name;
            this.TurnDelay = turnDelay;
            this.IsLearning = isLearning;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="AiPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        public void OnTurn(Game state)
        {
            OccupyGameAction a = null;

            Log.DebugFormat("[OnTurn] Player={0}",this.Name);

            // If board is empty, then we're going first
            if (state.Board.IsEmpty())
            {
                Log.DebugFormat("[OnTurn] First Move");
				// For testing sakes, we're going to pick a random location
				//   for now
                var xx = RngRandom.Instance.Next(0, 3);
                var yy = RngRandom.Instance.Next(0, 3);
                a = new OccupyGameAction(state, this, xx, yy,TurnDelay);
				state.PerformAction(a);
                return;
            }

            // If we're doing the second move
            if (state.GameActions.OfType<OccupyGameAction>().Count() == 1)
            {
                // Try and pick the center
                if (!state.Board.IsPositionOccupied(4))
                {
                    Log.DebugFormat("[OnTurn] Second Move take center");
                    a = new OccupyGameAction(state, this, 1, 1, TurnDelay);
                    state.PerformAction(a);
                    return;
                }
                
                // Try and pick a side
                var posavail = new[] {1, 3, 5, 7};
                var pos = posavail.FirstOrDefault(x => state.Board.IsPositionOccupied(x) == false);

                Log.DebugFormat("[OnTurn] Second Move take side {0}",pos);
                a = new OccupyGameAction(state, this, pos, TurnDelay);
                state.PerformAction(a);
                return;
            }

            // win if can
            var wmove = state.Board.WinLocation(this);
            if (wmove != null)
            {
                Log.DebugFormat("[OnTurn] Win Move {0}", wmove);
                a = new OccupyGameAction(state,this,wmove.Value,TurnDelay);
                state.PerformAction(a);
                return;
            }

            // block if can
            wmove = state.Board.WinLocation(state.Player1 == this ? state.Player2 : state.Player1);
            if (wmove != null)
            {
                Log.DebugFormat("[OnTurn] Block Move {0}", wmove);
                a = new OccupyGameAction(state, this, wmove.Value, TurnDelay);
                state.PerformAction(a);
                return;
            }

            if (state.StartPlayer == this)
            {
                // make horizontal line


                // make vertical line

                // make diagonal line
            }
            else
            {
                // make diagonal line

                // make horizontal line

                // make vertical line
            }
        }

        public override string ToString()
        {
            return Name;
        }
    }
}