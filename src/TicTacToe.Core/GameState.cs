namespace TicTacToe.Core
{
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Linq;

    using TicTacToe.Core.Annotations;

    public class GameState : INotifyPropertyChanged
    {
        private IPlayer playerTurn;

        public IPlayer Player1 { get; internal set; }
        public IPlayer Player2 { get; internal set; }
        public GameBoard Board { get; internal set; }

        /// <summary>
        /// List of actions taken during the game.
        /// </summary>
        public List<GameAction> GameActions { get; internal set; }

        /// <summary>
        /// Log of events that happen during the game.
        /// </summary>
        public List<string> GameLog { get; internal set; }

        /// <summary>
        /// Gets the <see cref="IPlayer"/> who's turn it is.
        /// </summary>
        public IPlayer PlayerTurn
        {
            get
            {
                return this.playerTurn;
            }
            internal set
            {
                if (Equals(value, this.playerTurn))
                {
                    return;
                }
                this.playerTurn = value;
                this.OnPropertyChanged("PlayerTurn");
            }
        }

        /// <summary>
        /// Create a new <see cref="GameState"/> with 2 players
        /// </summary>
        /// <param name="player1">Player 1</param>
        /// <param name="player2">Player 2</param>
        /// <param name="gameBoard">Game board to use</param>
        public GameState(IPlayer player1, IPlayer player2, GameBoard gameBoard)
        {
            GameLog = new List<string>();
            GameActions = new List<GameAction>();
            Player1 = player1;
            Player2 = player2;
            Board = gameBoard;

            // Randomly picks who the starting player will be
            // I think normally I would let the constructor of this class determine this
            //    , but for the sake of this project I'll just decide here.
            PlayerTurn = RngRandom.Instance.Next(0, 1) == 0 ? player1 : player2;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        [NotifyPropertyChangedInvocator]
        protected virtual void OnPropertyChanged(string propertyName)
        {
            var handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }

    public abstract class GameAction
    {
        internal GameState GameState { get; set; }

        public GameAction(GameState state)
        {
            GameState = state;
        }

        internal void Log(string message, params object[] args)
        {
            GameState.GameLog.Add(string.Format(message,args));
        }

        public abstract void Do();

        public abstract void Undo();
    }

    public class MoveGameAction : GameAction
    {
        public MoveGameAction(IPlayer player, GameState state):base(state)
        {
            
        }

        public override void Do()
        {
            throw new System.NotImplementedException();
        }

        public override void Undo()
        {
            throw new System.NotImplementedException();
        }
    }

    public class GameBoard
    {
        /// <summary>
        /// Positions and state of the board
        /// </summary>
        public IPlayer[][] BoardPositions { get; internal set; }

        public GameBoard()
        {
            //Create three rows of three board positions
            BoardPositions = Enumerable.Repeat(Enumerable.Repeat<IPlayer>(null, 3).ToArray(), 3).ToArray();
        }
    }

    public class HumanPlayer : IPlayer
    {
        public string Name { get; internal set; }

        /// <summary>
        /// Create a <see cref="HumanPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="HumanPlayer"/></param>
        public HumanPlayer(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="IPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        /// <returns>True to end the turn, False otherwise. Human players would return False, while AI would return True.</returns>
        public bool OnTurn(GameState state)
        {
            return false;
        }
    }

    public interface IPlayer
    {
        /// <summary>
        /// Name of the <cref see="IPlayer"/>
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Gets invoked when it's the <cref see="IPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        /// <returns>True to end the turn, False otherwise. Human players would return False, while AI would return True.</returns>
        bool OnTurn(GameState state);
    }
}
