namespace TicTacToe.Core.Actions
{
    using System;
    using System.Linq;
    using System.Threading;

    public class OccupyGameAction : GameAction
    {
        internal int X { get; set; }
        internal int Y { get; set; }
		internal int Move { get; set; }
        internal int Delay { get; set; }

        public OccupyGameAction(Game state, IPlayer player, int move, int delay = 0)
            : this(state, player,move % 3,move/3,delay)
        {
        }

        public OccupyGameAction(Game state, IPlayer player, int x, int y, int delay)
            : base(state, player)
        {
            if (x >= this.Game.Board.BoardPositions.First().Length)
                throw new ArgumentException("x must be between 0 and " + this.Game.Board.BoardPositions.First().Length, "x");
            if (y >= this.Game.Board.BoardPositions.First().Length)
                throw new ArgumentException("y must be between 0 and " + this.Game.Board.BoardPositions.Length, "y");
            this.X = x;
            this.Y = y;
            this.Move = (Y * 3) + X;
            this.Delay = delay;
        }

        public override void Do()
        {
            if (this.Game.Board.IsPositionOccupied(this.X, this.Y)) throw new InvalidOperationException("Position " + this.X + ":" + this.Y + " is already occupied.");

            this.Game.Board.Occupy(this.Player, this.X, this.Y);
            this.Log("{0} Occupy's {1}:{2}", this.Player, this.X, this.Y);
            //Thread.Sleep(Delay);
        }
    }
}