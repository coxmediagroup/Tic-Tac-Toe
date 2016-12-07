using TicTacToe.Core.Players;

namespace TicTacToe.Core
{
    using System;

    public abstract class GameAction
    {
        internal Game Game { get; set; }
        internal IPlayer Player { get; set; }

        protected GameAction(Game state, IPlayer player)
        {
            if (state == null) throw new ArgumentException("state cannot be null.", "state");
            if (player == null) throw new ArgumentException("player cannot be null.", "player");
            Game = state;
            Player = player;
        }

        internal void Log(string message, params object[] args)
        {
            Game.ActionLog(string.Format(message, args));
        }

        public abstract void Do();
    }
}