namespace TicTacToe.Core.Actions
{
    using System;
    using System.Linq;

    public class PassTurnGameAction : GameAction
    {
        public PassTurnGameAction(GameState state, IPlayer player)
            : base(state, player)
        {
        }

        public override void Do()
        {
            if(this.GameState.PlayerTurn != this.Player)
                throw new InvalidOperationException("Only the active player can pass the turn.");
            if (this.GameState.GameActions.Last().Player != this.Player) 
                throw new InvalidOperationException("Player must perform an action before passing their turn.");
            this.GameState.PlayerTurn = this.GameState.PlayerTurn == this.GameState.Player1 
                ? this.GameState.Player2 
                : this.GameState.Player1;
            this.Log("{0} Passes turn to {1}", this.Player, this.GameState.PlayerTurn);
        }
    }
}