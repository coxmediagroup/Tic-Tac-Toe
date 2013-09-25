using System.Linq;
using TicTacToe.Core.Actions;
using TicTacToe.Core.Utils;

namespace TicTacToe.Core
{
    public static class AiStateMachine
    {
        public static MoveItem GetNextMove(Game game, IPlayer me)
        {
            var mcount = game.GameActions.OfType<OccupyGameAction>().Count();
            var startGameMove = game.GameActions.OfType<OccupyGameAction>().FirstOrDefault();
            var lastPlayerMove = game.GameActions.OfType<OccupyGameAction>().LastOrDefault();
            if (game.StartPlayer == me)
            {
                // If we started the game
                // Go for a win first, or tie second
                // Play aggressively so the other player doesn't have a choice but to always block
                switch (mcount)
                {
                    case 0:
                    {
                        // Almost thing that we should only pick corners
                        //    With corners we can win 87.5% of the time,
                        //    The rest are 50%
                        var next = RngRandom.Instance.Next(0, 9);
                        return new MoveItem(next, me);
                        break;
                    }
                    case 2:
                    {
                        switch (startGameMove.Move)
                        {
                            // Corners
                            case 0:
                            case 2:
                            case 6:
                            case 8:
                            {
                                break;
                            }
                            // Sides
                            case 1:
                            case 3:
                            case 5:
                            case 7:
                            {
                                break;
                            }
                            // Center
                            case 4:
                            {
                                break;
                            }
                        }
                        break;
                    }
                    case 4:
                    {
                        // win game immediately(all moves can be won on this turn)
                        // Or fall through
                        break;
                    }
                    default:
                    {
                        // Pick next move(blocking, then forcing to end)
                        break;
                    }
                }
            }
            else
            {
                // If the other player started the game
                // Go for a tie first, win second
            }
            return null;
        }
    }
}