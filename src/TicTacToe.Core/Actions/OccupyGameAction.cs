using System.Threading;
using TicTacToe.Core.Players;

namespace TicTacToe.Core.Actions
{
    using System;
    using System.Linq;

    public class OccupyGameAction : GameAction
    {
        internal int X { get; set; }
        internal int Y { get; set; }
		internal int Move { get; set; }
        internal int Delay { get; set; }

        public OccupyGameAction(Game state, IPlayer player, int move, int delay = 0)
            : this(state, player,move % 3,move/3,delay)
        {
            if (move >= 9)
                throw new ArgumentException("move must be between 0 and 8", "move");
        }

        public OccupyGameAction(Game state, IPlayer player, int x, int y, int delay)
            : base(state, player)
        {
            if (x >= Game.Board.BoardPositions.First().Length)
                throw new ArgumentException("x must be between 0 and " + Game.Board.BoardPositions.First().Length, "x");
            if (y >= Game.Board.BoardPositions.First().Length)
                throw new ArgumentException("y must be between 0 and " + Game.Board.BoardPositions.Length, "y");
            X = x;
            Y = y;
            Move = (Y * 3) + X;
            Delay = delay;
        }

        public override void Do()
        {
            if (Game.Board.IsPositionOccupied(X, Y)) throw new InvalidOperationException("Position " + X + ":" + Y + " is already occupied.");

            Game.Board.Occupy(Player, X, Y);
            Log("{0} Occupy's {1}:{2}", Player, X, Y);
            Thread.Sleep(Delay);
        }
    }
}