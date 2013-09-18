﻿namespace TicTacToe.Core
{
    using System;
    using System.Security;

    public class PassTurnGameAction : GameAction
    {
        public PassTurnGameAction(GameState state, IPlayer player)
            : base(state, player)
        {
        }

        public override void Do()
        {
            if(GameState.PlayerTurn != Player)
                throw new InvalidOperationException("Only the active player can pass the turn.");
            GameState.PlayerTurn = GameState.PlayerTurn == GameState.Player1 
                ? GameState.Player2 
                : GameState.Player1;
            Log("{0} Passes turn to {1}", Player, GameState.PlayerTurn);
        }
    }
}