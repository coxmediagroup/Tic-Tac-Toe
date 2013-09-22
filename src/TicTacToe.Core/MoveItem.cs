namespace TicTacToe.Core
{
    using System;

    public class MoveItem : IEquatable<MoveItem>
    {
        public int Move { get; set; }
		public int X { get; set; }
		public int Y { get; set; }
        public IPlayer Player { get; set; }

        public MoveItem(int move, IPlayer player)
        {
            this.Move = move;
            this.Player = player;
            this.X = move % 3;
            this.Y = move / 3;
        }

        public void RotateLeft()
        {
            var x = Y;
            var y = 3 - X - 1;
            X = x;
            Y = y;
            Move = (Y * 3) + X;
        }

        public void FlipHorizontally()
        {
            var x = 3 - X - 1;
            var y = Y;
            X = x;
            Y = y;
            Move = (Y * 3) + X;
        }

        public bool Equals(MoveItem other)
        {
            return this.Move == other.Move && this.Player == other.Player;
        }
    }
}