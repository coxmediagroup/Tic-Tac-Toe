namespace TicTacToe.Core.Actions
{
    public class ResetGameAction : GameAction
    {
        public ResetGameAction(GameState state, IPlayer player)
            : base(state, player)
        {
        }

        public override void Do()
        {
            this.GameState.Reset();
            this.Log("{} Resets the game", this.Player);
        }
    }
}