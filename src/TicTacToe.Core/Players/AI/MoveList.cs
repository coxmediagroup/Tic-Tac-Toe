using System;
using System.Collections.Generic;
using System.Linq;
using TicTacToe.Core.Actions;

namespace TicTacToe.Core.Players.AI
{
    public class MoveList : ICloneable
    {
        public IPlayer StartPlayer { get; set; }
        public int MoveCount { get; set; }
        public List<MoveItem> Moves { get; set; }

        public MoveList()
        {
            Moves = new List<MoveItem>();
            MoveCount = 0;
            StartPlayer = null;
        }

        public MoveList(Game game)
        {
            var moves = game.GameActions.OfType<OccupyGameAction>();
            Moves = moves.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            MoveCount = Moves.Count;
            StartPlayer = game.StartPlayer;
        }

        public void RotateLeft()
        {
            Moves.ForEach(x => x.RotateLeft());
        }

        public void FlipHorizontally()
        {
            Moves.ForEach(x => x.FlipHorizontally());
        }

        public void AlignTo(MoveList list)
        {
            if (list.MoveCount == 0)
                return;
            foreach (var t in GetTransforms())
            {
                var match = true;
                for (var i = 0; i < (list.MoveCount > MoveCount ? list.MoveCount : MoveCount); i++)
                {
                    if (list.Moves[i] != Moves[i])
                    {
                        match = false;
                        break;
                    }
                }
                if (match)
                {
                    this.Moves = t.Moves;
                    return;
                }
            }
        }

        public void CorrectTransform()
        {
            if (MoveCount == 0)
                return;
            if (Moves[0].IsCenter && MoveCount == 1)
                return;
            if (Moves[0].IsCenter)
            {
                if (Moves[1].IsCorner)
                {
                    while (Moves[1].Move != 0)
                    {
                        RotateLeft();
                    }
                }
                else if (Moves[1].IsSide)
                {
                    while (Moves[1].Move != 1)
                    {
                        RotateLeft();
                    }
                }
                return;
            }

            if (Moves[0].IsCorner)
            {
                while (Moves[0].Move != 0)
                {
                    RotateLeft();
                }
                if (Moves[1].IsCorner)
                {
                    if (Moves[1].Move == 6)
                    {
                        FlipHorizontally();
                        RotateLeft();
                    }
                }
                else if (Moves[1].IsSide)
                {
                    if (Moves[1].Move == 7 || Moves[1].Move == 3)
                    {
                        FlipHorizontally();
                        RotateLeft();
                    }
                }
                return;
            }
            if (Moves[0].IsSide)
            {
                while (Moves[0].Move != 1)
                {
                    RotateLeft();
                }
                if (Moves[1].IsCorner)
                {
                    if (Moves[1].Move == 2)
                    {
                        FlipHorizontally();
                    }
                    else if (Moves[1].Move == 8)
                    {
                        FlipHorizontally();
                    }
                }
                else if (Moves[1].IsSide)
                {
                    if (Moves[1].Move == 5)
                    {
                        FlipHorizontally();
                    }
                }
            }
        }

        public IEnumerable<MoveList> GetTransforms()
        {
            var m2 = this.Clone() as MoveList;
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.RotateLeft();
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.FlipHorizontally();
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.RotateLeft();
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.RotateLeft();
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.RotateLeft();
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.FlipHorizontally();
            yield return m2;
            m2 = m2.Clone() as MoveList; 
            m2.RotateLeft();
            yield return m2;
            //This last line will put it back to its original state, not sure if that's necessary.
            //m2 = m2.Clone() as MoveList; 
            //m2.RotateLeft();
            //yield return m2;
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
            var ml = new MoveList();
            ml.StartPlayer = this.StartPlayer;
            ml.MoveCount = this.MoveCount;
            ml.Moves = this.Moves.Select(x => x.Clone() as MoveItem).ToList();
            return ml;
        }

        #endregion
    }
}