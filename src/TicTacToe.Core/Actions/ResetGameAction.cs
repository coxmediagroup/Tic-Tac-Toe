namespace TicTacToe.Core.Actions
{
    public class ResetGameAction : GameAction
    {
        public ResetGameAction(Game state, IPlayer player)
            : base(state, player)
        {
        }

        public override void Do()
        {
            this.Game.Reset();
            this.Log("{} Resets the game", this.Player);
        }
    }
}