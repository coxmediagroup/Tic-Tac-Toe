namespace TicTacToe.Core.Actions
{
    using System;
    using System.Linq;

    public class PassTurnGameAction : GameAction
    {
        public PassTurnGameAction(Game state, IPlayer player)
            : base(state, player)
        {
        }

        public override void Do()
        {
            if(this.Game.PlayerTurn != this.Player)
                throw new InvalidOperationException("Only the active player can pass the turn.");
            if (this.Game.GameActions.Last().Player != this.Player) 
                throw new InvalidOperationException("Player must perform an action before passing their turn.");
            this.Game.PlayerTurn = this.Game.PlayerTurn == this.Game.Player1 
                ? this.Game.Player2 
                : this.Game.Player1;
            this.Log("{0} Passes turn to {1}", this.Player, this.Game.PlayerTurn);
            if (this.Game.PlayerTurn.OnTurn(this.Game))
            {
                var action = new PassTurnGameAction(this.Game, this.Game.PlayerTurn);
                this.Game.PerformAction(action);
            }
        }
    }
}