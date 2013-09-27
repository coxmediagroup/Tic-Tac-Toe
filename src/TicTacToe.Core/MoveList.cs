using System;
using System.Collections.Generic;
using System.Linq;
using TicTacToe.Core.Actions;
using TicTacToe.Core.Players;

namespace TicTacToe.Core
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
                    Moves = t.Moves;
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
// ReSharper disable PossibleNullReferenceException
            var m2 = Clone() as MoveList;
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
// ReSharper restore PossibleNullReferenceException
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
// ReSharper disable once UseObjectOrCollectionInitializer
            var ml = new MoveList();
            ml.StartPlayer = StartPlayer;
            ml.MoveCount = MoveCount;
            ml.Moves = Moves.Select(x => x.Clone() as MoveItem).ToList();
            return ml;
        }

        #endregion
    }
}