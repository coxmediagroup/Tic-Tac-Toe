using System.Threading;
using FakeItEasy;

namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Threading.Tasks;

    using Common.Logging;

    using TicTacToe.Core.Actions;
    using TicTacToe.Core.Annotations;
    using TicTacToe.Core.Utils;

    public class Game : INotifyPropertyChanged
    {
        internal static ILog GameLogger = LogManager.GetLogger("GameLog");

        private IPlayer playerTurn;
        private GameStatus status;
        private GameWinStatus winStatus;
        private IPlayer winner;
        private IPlayer _player1;
        private IPlayer _player2;

        public IPlayer Player1
        {
            get { return _player1; }
            set
            {
                if (Equals(value, _player1)) return;
                _player1 = value;
                OnPropertyChanged("Player1");
            }
        }

        public IPlayer Player2
        {
            get { return _player2; }
            set
            {
                if (Equals(value, _player2)) return;
                _player2 = value;
                OnPropertyChanged("Player2");
            }
        }

        public GameBoard Board { get; internal set; }

        /// <summary>
        /// List of actions taken during the game.
        /// </summary>
        public List<GameAction> GameActions { get; internal set; }

        /// <summary>
        /// Log of events that happen during the game.
        /// </summary>
        public List<string> GameLog { get; internal set; }

		public LearnProcessor LearnProcessor { get; internal set; }

		public IPlayer StartPlayer { get; internal set; }

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
                if (this.playerTurn != null)
                {

                    this.playerTurn.OnTurn(this);
                }
            }
        }

        public GameStatus Status
        {
            get
            {
                return this.status;
            }
            internal set
            {
                if (value == this.status)
                {
                    return;
                }
                this.status = value;
                this.OnPropertyChanged("Status");
            }
        }

        public GameWinStatus WinStatus
        {
            get
            {
                return this.winStatus;
            }
            internal set
            {
                if (value == this.winStatus)
                {
                    return;
                }
                this.winStatus = value;
                this.OnPropertyChanged("WinStatus");
            }
        }

        public IPlayer Winner
        {
            get
            {
                return this.winner;
            }
            internal set
            {
                if (Equals(value, this.winner))
                {
                    return;
                }
                this.winner = value;
                this.OnPropertyChanged("Winner");
            }
        }

        /// <summary>
        /// Create a new <see cref="Game"/> with 2 players
        /// </summary>
        /// <param name="player1">Player 1</param>
        /// <param name="player2">Player 2</param>
        /// <param name="gameBoard">Game board to use</param>
        public Game(IPlayer player1, IPlayer player2)
        {
            if (player1 == null)
                throw new ArgumentException("player1 can't be null", "player1");
            if (player2 == null)
                throw new ArgumentException("player2 can't be null", "player2");
            LearnProcessor = new LearnProcessor("aidata.dat");
            GameLog = new List<string>();
            GameActions = new List<GameAction>();
            Player1 = player1;
            Player2 = player2;
            Reset();
        }

        public void Start(IPlayer startPlayer = null)
        {
            if (startPlayer != null)
            {
                PlayerTurn = startPlayer;
                StartPlayer = startPlayer;
                return;
            }
            if (PlayerTurn == null)
            {
                // Randomly picks who the starting player will be
                // I think normally I would let the constructor of this class determine this
                //    , but for the sake of this project I'll just decide here.
                var rnum = RngRandom.Instance.Next(0, 2);
                var tp = rnum == 0 ? Player1 : Player2;
                PlayerTurn = tp;
            }
            else
            {
                var tp = PlayerTurn == Player1 ? Player2 : Player1;
                PlayerTurn = tp;
            }
            StartPlayer = PlayerTurn;
        }

        public void PerformAction(GameAction action)
        {
            if (action == null)
                throw new ArgumentOutOfRangeException("action", "action can not be null");
            if (Status != GameStatus.Running && (action is ResetGameAction) == false)
                throw new InvalidOperationException("Cannot do that action because the game is finished.");
            if ((action is ResetGameAction) == false && action.Player != PlayerTurn)
                throw new InvalidOperationException("It's not " + action.Player.Name + "'s turn");
            GameActions.Add(action);
            action.Do();
            OnPropertyChanged("GameActions");
            OnPropertyChanged("GameLog");
            CheckGameState();
            if (Status == GameStatus.Running)
            {
                Task.Factory.StartNew(() =>
                {
                    if (action is OccupyGameAction)
                    {
                        Thread.Sleep((action as OccupyGameAction).Delay);
                    }
                    PlayerTurn = PlayerTurn == Player1 ? Player2 : Player1;
                });
            }
        }

        /// <summary>
        /// Checks and updates the game state based on previous actions
        /// </summary>
        internal void CheckGameState()
        {
            var boardWinner = Board.Winner();
            if (boardWinner != null)
            {
                WinStatus = GameWinStatus.Win;
                Winner = boardWinner;
            }
            else
            {
                if (!this.Board.IsFull())
                    return;
                this.WinStatus = GameWinStatus.Tie;
                this.Winner = null;
            }
            this.ActionLog(string.Format("Game Finished[{0}]: {1}", WinStatus, Winner));
            Status = GameStatus.Finished;
			LearnProcessor.ProcessEndGame(this);
        }

        public void Reset()
        {
            Status = GameStatus.Running;
            WinStatus = GameWinStatus.None;
            Winner = null;
            Board = new GameBoard();
            GameActions = new List<GameAction>();
            GameLog = new List<string>();

            OnPropertyChanged("Board");
            OnPropertyChanged("GameActions");
            OnPropertyChanged("GameLog");
        }

        internal void ActionLog(string message)
        {
            GameLogger.Info(message);
            GameLog.Add(message);
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

    public enum GameStatus
    {
        Running,
        Finished
    }

    public enum GameWinStatus
    {
        None = 0,
        Win = 1,
        Tie = 2
    }
}
