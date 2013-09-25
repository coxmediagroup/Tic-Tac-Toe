using System;

namespace TicTacToe.Core.Players.AI
{
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
            var oy = Y;
            Y = 3 - X - 1;
            X = oy;
            Move = (Y * 3) + X;
        }

        public void FlipHorizontally()
        {
            X = 3 - X - 1;
            Move = (Y * 3) + X;
        }

        public bool Equals(MoveItem other)
        {
            return this.Move == other.Move && this.Player == other.Player;
        }
    }
}