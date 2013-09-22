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

        public bool Equals(MoveItem other)
        {
            return this.Move == other.Move && this.Player == other.Player;
        }
    }
}