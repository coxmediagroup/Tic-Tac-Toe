namespace TicTacToe.Core
{
    using System;
    using System.Collections.ObjectModel;
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
        public ObservableCollection<GameAction> GameActions { get; internal set; }

        /// <summary>
        /// Log of events that happen during the game.
        /// </summary>
        public ObservableCollection<string> GameLog { get; internal set; }

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
            GameLog = new ObservableCollection<string>();
            GameActions = new ObservableCollection<GameAction>();
            Player1 = player1;
            Player2 = player2;
            Board = gameBoard;

            // Randomly picks who the starting player will be
            // I think normally I would let the constructor of this class determine this
            //    , but for the sake of this project I'll just decide here.
            PlayerTurn = RngRandom.Instance.Next(0, 1) == 0 ? player1 : player2;
        }

        public void PerformAction(GameAction action)
        {
            GameActions.Add(action);
            action.Do();
        }

        internal void Reset()
        {
            Board = new GameBoard();
            PlayerTurn = RngRandom.Instance.Next(0, 1) == 0 ? Player1 : Player2;
            OnPropertyChanged("Board");
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
        internal IPlayer Player { get; set; }

        public GameAction(GameState state, IPlayer player)
        {
            GameState = state;
            Player = player;
        }

        internal void Log(string message, params object[] args)
        {
            GameState.GameLog.Add(string.Format(message,args));
        }

        public abstract void Do();
    }

    public class OccupyGameAction : GameAction
    {
        internal int X { get; set; }
        internal int Y { get; set; }

        public OccupyGameAction(IPlayer player, GameState state, int x, int y):base(state, player)
        {
            if (state == null) throw new ArgumentException("state cannot be null.", "state");
            if (player == null) throw new ArgumentException("player cannot be null.", "player");
            if (x >= GameState.Board.BoardPositions.First().Length)
                throw new ArgumentException("x must be between 0 and " + GameState.Board.BoardPositions.First().Length, "x");
            if (y >= GameState.Board.BoardPositions.First().Length)
                throw new ArgumentException("y must be between 0 and " + GameState.Board.BoardPositions.Length, "y");
            Player = player;
            X = x;
            Y = y;
        }

        public override void Do()
        {
            if (GameState.Board.IsPositionOccupied(X, Y)) 
                throw new InvalidOperationException("Position " + X + ":" + Y + " is already occupied.");

            GameState.Board.Occupy(Player, X, Y);
            Log("{0} Occupy's {1}:{2}",Player,X,Y);
        }
    }

    public class ResetGameAction : GameAction
    {
        public ResetGameAction(GameState state, IPlayer player)
            : base(state, player)
        {
        }

        public override void Do()
        {
            GameState.Reset();
            Log("{} Resets the game", Player);
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

        public bool IsPositionOccupied(int x, int y)
        {
            return BoardPositions[y][x] != null;
        }

        public void Occupy(IPlayer player, int x, int y)
        {
            if (IsPositionOccupied(x, y))
                throw new InvalidOperationException("Position " + x + ":" + y + " is already occupied.");
            BoardPositions[y][x] = player;
        }

        public void UnOccupy(int x, int y)
        {
            BoardPositions[y][x] = null;
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

        public override string ToString()
        {
            return Name;
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
