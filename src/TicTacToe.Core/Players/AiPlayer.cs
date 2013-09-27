using System;
using System.Linq;
using System.Management.Instrumentation;
using System.Net.NetworkInformation;
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
                
                // Try and pick a corner
                var posavail = new[] {0, 2, 6, 8};
                var pos = posavail.FirstOrDefault(x => state.Board.IsPositionOccupied(x) == false);

                Log.DebugFormat("[OnTurn] Second Move take corner {0}",pos);
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

            int? move = null;

            if (state.StartPlayer == this)
            {
                // make diagonal line
                move = TryMakeLine(state, this, true, DiagonalLines);

                // make vertical line
                if (move == null)
                    move = TryMakeLine(state, this, false, VerticalLines);

                // make horizontal line
                if (move == null)
                    move = TryMakeLine(state, this, false, HorizontalLines);

                if (move != null)
                {
                    Log.DebugFormat("[OnTurn] SP Line Move {0}", move);
                    a = new OccupyGameAction(state, this, move.Value, TurnDelay);
                    state.PerformAction(a);
                    return;
                }
            }
            else
            {
                // make diagonal line
                move = TryMakeLine(state, this, true, DiagonalLines);

                // make horizontal line - Don't skip center if on side
                if (move == null)
                    move = TryMakeLine(state, this, false, HorizontalLines);

                // make vertical line - Don't skip center if on side
                if (move == null)
                    move = TryMakeLine(state, this, false, VerticalLines);

                if (move != null)
                {
                    Log.DebugFormat("[OnTurn] SecP Line Move {0}", move);
                    a = new OccupyGameAction(state, this, move.Value, TurnDelay);
                    state.PerformAction(a);
                    return;
                }
            }

            // Ok, so can't take start moves, win, block, or make any lines, at this point we just pick the first possible location on the board

            for (var i = 0; i < 9; i++)
            {
                if (state.Board.IsPositionOccupied(i) == false)
                {
                    Log.DebugFormat("[OnTurn] Blind Move {0}", i);
                    a = new OccupyGameAction(state, this, i, TurnDelay);
                    state.PerformAction(a);
                    return;
                }
            }
            throw new InvalidOperationException("[OnTurn] No Possible Moves?");
        }

        internal static readonly int[][] HorizontalLines = { new[] { 0, 1, 2 }, new[] { 3, 4, 5 }, new[] { 6, 7, 8 } };
        internal static readonly int[][] VerticalLines = { new[] { 0, 3, 6 }, new[] { 1, 4, 7 }, new[] { 2, 5, 8 } };
        internal static readonly int[][] DiagonalLines = { new[] { 0, 4, 8 }, new[] { 2, 4, 6 } };

        internal int? TryMakeLine(Game state, IPlayer player, bool skipCenter, int[][] possibleLines)
        {
            int? ret = null;
            var ourMoves = state.GameActions.OfType<OccupyGameAction>().Where(x => x.Player == player).ToList();
            var centers = possibleLines.Select(x => x.Skip(1).Take(1).First()).ToArray();

            foreach (var move in ourMoves)
            {
                // find a line we're a part of
                var mv = move;
                var ourLines = possibleLines.Where(x => x.Contains(mv.Move));
                foreach (var ourLine in ourLines)
                {
                    if (ourLine == null)
                        continue;
                    bool gotIt = true;
                    foreach (var p in ourLine)
                    {
                        var pos = state.Board.GetPosition(p);
                        if (pos == null) continue;
                        if (pos != player)
                        {
                            gotIt = false;
                            break;
                        }
                    }
                    if (gotIt)
                    {
                        if ((centers.Contains(move.Move)) || skipCenter || new MoveItem(move.Move,this).IsSide)
                        {
                            if (ourLine[1] != move.Move)
                            {
                                return ourLine[1];
                            }
                            ret = ourLine.First(x => state.Board.IsPositionOccupied(x) == false);
                            return ret;
                        }

                        if (move.Move == ourLine.First())
                            ret = ourLine.Last();
                        else ret = ourLine.First();
                        return ret;
                    }
                }
                // If we get here that means that there wasn't a line that was completely free for us to use with this move.
            }
            return ret;
        }

        public override string ToString()
        {
            return Name;
        }
    }
}