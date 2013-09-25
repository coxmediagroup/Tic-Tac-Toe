using System.Linq;
using TicTacToe.Core.Actions;
using TicTacToe.Core.Utils;

namespace TicTacToe.Core.Players.AI.StateMachine
{
    public class AiStateMachine : IMoveStateMachine
    {
        #region Singleton

        internal static AiStateMachine SingletonContext { get; set; }

        private static readonly object AiStateMachineSingletonLocker = new object();

        public static AiStateMachine Instance
        {
            get
            {
                if (SingletonContext == null)
                {
                    lock (AiStateMachineSingletonLocker)
                    {
                        if (SingletonContext == null)
                        {
                            SingletonContext = new AiStateMachine();
                        }
                    }
                }
                return SingletonContext;
            }
        }

        #endregion Singleton

        public MoveItem GetNextMove(Game game, IPlayer me)
        {
            // If no moves then go first
            if (!game.GameActions.OfType<OccupyGameAction>().Any())
            {
                // Almost think that we should only pick corners
                //    With corners we can win 87.5% of the time,
                //    The rest are 50%
                var next = RngRandom.Instance.Next(0, 9);
                return new MoveItem(next, me);
            }

            var startGameMove = game.GameActions.OfType<OccupyGameAction>().FirstOrDefault();
            switch (startGameMove.Move)
            {
                case 0:
                case 2:
                case 6:
                case 8:
                    {
                        return new CornerStartStateMachine().GetNextMove(game, me);
                    }
                case 1:
                case 3:
                case 5:
                case 7:
                    {
                        return new SideStartStateMachine().GetNextMove(game, me);
                    }
                case 4:
                    {
                        return new CenterStartStateMachine().GetNextMove(game, me);
                    }
            }
        }
    }

    public class CornerStartStateMachine : IMoveStateMachine
    {
        public MoveItem GetNextMove(Game game, IPlayer me)
        {

        }
    }

    public class SideStartStateMachine : IMoveStateMachine
    {
        public MoveItem GetNextMove(Game game, IPlayer me)
        {

        }
    }

    public class CenterStartStateMachine : IMoveStateMachine
    {
        public MoveItem GetNextMove(Game game, IPlayer me)
        {

        }
    }
}