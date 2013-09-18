namespace TicTacToe.Core
{
    public abstract class GameAction
    {
        internal GameState GameState { get; set; }
        internal IPlayer Player { get; set; }

        protected GameAction(GameState state, IPlayer player)
        {
            this.GameState = state;
            this.Player = player;
        }

        internal void Log(string message, params object[] args)
        {
            this.GameState.GameLog.Add(string.Format(message,args));
        }

        public abstract void Do();
    }
}