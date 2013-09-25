namespace TicTacToe.Core.Players.AI.StateMachine
{
    public interface IMoveStateMachine
    {
        MoveItem GetNextMove(Game game, IPlayer me);
    }
}