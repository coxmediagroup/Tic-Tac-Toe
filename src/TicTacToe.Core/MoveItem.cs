using System;
using TicTacToe.Core.Players;

namespace TicTacToe.Core
{
    public class MoveItem : IEquatable<MoveItem>, ICloneable
    {
        public int Move { get; set; }
		public int X { get; set; }
		public int Y { get; set; }
        public IPlayer Player { get; set; }

        public bool IsCorner
        {
            get
            {
                return Move == 0 || Move == 2 || Move == 6 || Move == 8;
            }
        }

        public bool IsSide
        {
            get
            {
                return Move == 1 || Move == 3 || Move == 5 || Move == 7;
            }
        }

        public bool IsCenter
        {
            get
            {
                return Move == 4;
            }
        }

        public MoveItem(int move, IPlayer player)
        {
            Move = move;
            Player = player;
            X = move % 3;
            Y = move / 3;
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
            return Move == other.Move && Player == other.Player;
        }

        #region Implementation of ICloneable

        /// <summary>
        /// Creates a new object that is a copy of the current instance.
        /// </summary>
        /// <returns>
        /// A new object that is a copy of this instance.
        /// </returns>
        public object Clone()
        {
            return new MoveItem(Move, Player);
        }

        #endregion
    }
}