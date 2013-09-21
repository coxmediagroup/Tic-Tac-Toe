﻿using System.Linq.Expressions;
using System.Security.Cryptography.X509Certificates;
using System.Xaml;

namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    using TicTacToe.Core.Actions;
    using TicTacToe.Core.Utils;

    public class AiPlayer : IPlayer
    {
        public string Name { get; internal set; }
		public int TurnDelay { get; set; }

        /// <summary>
        /// Create a <see cref="AiPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="AiPlayer"/></param>
        /// <param name="focus">Choose what the Ai is more focused on achieving</param>
        /// <param name="turnDelay">Time to wait before switching the turn in ms(Default: 0)</param>
        public AiPlayer(string name, int turnDelay = 0)
        {
            this.Name = name;
            this.TurnDelay = turnDelay;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="AiPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        public void OnTurn(Game state)
        {
            // If board is empty, then we're going first
            if (state.Board.IsEmpty())
            {
				// For testing sakes, we're going to pick a random location
				//   for now
                var xx = RngRandom.Instance.Next(0, 3);
                var yy = RngRandom.Instance.Next(0, 3);
                var a = new OccupyGameAction(state, this, xx, yy,TurnDelay);
				state.PerformAction(a);
                return;
            }

			// Otherwise, things get a bit sticky here.
			// I suppose we can brute force this sucker and see
			//    how long it takes first.

            //var act = new OccupyGameAction(state, this, x, y, TurnDelay);
            //state.PerformAction(act);
        }

        public override string ToString()
        {
            return Name;
        }
    }
}