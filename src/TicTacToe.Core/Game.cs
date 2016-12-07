using System.Threading;
using TicTacToe.Core.Players;

namespace TicTacToe.Core
{
    using System;
    using System.Collections.Concurrent;
    using System.Collections.Generic;
    using System.ComponentModel;
    using Common.Logging;

    using Actions;
    using Annotations;
    using Utils;

    public class Game : INotifyPropertyChanged, IDisposable
    {
        internal static ILog GameLogger = LogManager.GetLogger("GameLog");

        private IPlayer _playerTurn;
        private GameStatus _status;
        private GameWinStatus _winStatus;
        private IPlayer _winner;
        private IPlayer _player1;
        private IPlayer _player2;

        internal Thread ActionThread;
        internal ConcurrentQueue<GameAction> ActionQueue;
        internal bool IsRunning = true;

        public bool ReadyForReset { get; set; }

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

        public IPlayer StartPlayer { get; internal set; }

        /// <summary>
        /// Gets the <see cref="IPlayer"/> who's turn it is.
        /// </summary>
        public IPlayer PlayerTurn
        {
            get
            {
                return _playerTurn;
            }
            internal set
            {
                if (Equals(value, _playerTurn))
                {
                    return;
                }
                //ActionGate.WaitOne();
                _playerTurn = value;
                OnPropertyChanged("PlayerTurn");
            }
        }

        public GameStatus Status
        {
            get
            {
                return _status;
            }
            internal set
            {
                if (value == _status)
                {
                    return;
                }
                _status = value;
                OnPropertyChanged("Status");
            }
        }

        public GameWinStatus WinStatus
        {
            get
            {
                return _winStatus;
            }
            internal set
            {
                if (value == _winStatus)
                {
                    return;
                }
                _winStatus = value;
                OnPropertyChanged("WinStatus");
            }
        }

        public IPlayer Winner
        {
            get
            {
                return _winner;
            }
            internal set
            {
                if (Equals(value, _winner))
                {
                    return;
                }
                _winner = value;
                OnPropertyChanged("Winner");
            }
        }

        /// <summary>
        /// Create a new <see cref="Game"/> with 2 players
        /// </summary>
        /// <param name="player1">Player 1</param>
        /// <param name="player2">Player 2</param>
        public Game(IPlayer player1, IPlayer player2)
        {
            if (player1 == null)
                throw new ArgumentException("player1 can't be null", "player1");
            if (player2 == null)
                throw new ArgumentException("player2 can't be null", "player2");
            GameLog = new List<string>();
            GameActions = new List<GameAction>();
            Player1 = player1;
            Player2 = player2;
            Reset();
            ActionThread = new Thread(ActionThreadRun);
            ActionThread.Start();
        }

        public void Start(IPlayer startPlayer = null)
        {
            if (startPlayer != null)
            {
                PlayerTurn = startPlayer;
                StartPlayer = startPlayer;
                LogManager.GetCurrentClassLogger().Debug("DoTurn 1");
                DoTurn(PlayerTurn);
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
            LogManager.GetCurrentClassLogger().Debug("DoTurn 2");
            DoTurn(PlayerTurn);
        }

        public void PerformAction(GameAction action)
        {
            lock (this)
            {
                if (action == null)
                    throw new ArgumentOutOfRangeException("action", "action can not be null");
                if (Status != GameStatus.Running)
                    throw new InvalidOperationException("Cannot do that action because the game is finished.");
                if (action.Player != PlayerTurn)
                    throw new InvalidOperationException("It's not " + action.Player.Name + "'s turn");
                LogManager.GetCurrentClassLogger().Debug("EnqueueAction");
                ActionQueue.Enqueue(action);
            }
        }

        public void DoTurn(IPlayer player, int delay = 0)
        {
            if (_playerTurn != null)
            {
                _playerTurn.OnTurn(this);
            }
        }

        internal void ActionThreadRun()
        {
            while (IsRunning)
            {
                GameAction action;
                if (!ActionQueue.TryDequeue(out action))
                {
                    Thread.Sleep(1);
                    continue;
                }
                if (Status == GameStatus.Running)
                {
                    ReadyForReset = false;
                    if (action is OccupyGameAction)
                        LogManager.GetCurrentClassLogger()
                            .DebugFormat("DoAction[{0}] {1}:{2}", action.GetType().Name, (action as OccupyGameAction).X, (action as OccupyGameAction).Y);
                    action.Do();
                    GameActions.Add(action);
                    OnPropertyChanged("GameActions");
                    OnPropertyChanged("GameLog");
                    CheckGameState();
                    if (Status == GameStatus.Finished)
                    {
                        LogManager.GetCurrentClassLogger().DebugFormat("Finished with {0} in queue", ActionQueue.Count);
                        Thread.Sleep(10);
                        ReadyForReset = true;
                        continue;
                    }
                    var delay = 0;
                    if (action is OccupyGameAction)
                    {
                        delay = (action as OccupyGameAction).Delay;
                    }
                    PlayerTurn = PlayerTurn == Player1 ? Player2 : Player1;
                    LogManager.GetCurrentClassLogger().Debug("DoTurn 3");
                    DoTurn(PlayerTurn, delay);
                }
                else Thread.Sleep(10);
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
                if (!Board.IsFull())
                    return;
                WinStatus = GameWinStatus.Tie;
                Winner = null;
            }
            ActionLog(string.Format("Game Finished[{0}]: {1}", WinStatus, Winner));
            Status = GameStatus.Finished;
        }

        public void Reset()
        {
            Status = GameStatus.Running;
            WinStatus = GameWinStatus.None;
            Winner = null;
            Board = new GameBoard();
            GameActions = new List<GameAction>();
            GameLog = new List<string>();
            ActionQueue = new ConcurrentQueue<GameAction>();

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

        public void Dispose()
        {
            IsRunning = false;
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
