namespace TicTacToe.Core
{
    using System.Collections.Generic;
    using System.ComponentModel;

    using TicTacToe.Core.Annotations;
    using TicTacToe.Core.Utils;

    public class Game : INotifyPropertyChanged
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
        /// Create a new <see cref="Game"/> with 2 players
        /// </summary>
        /// <param name="player1">Player 1</param>
        /// <param name="player2">Player 2</param>
        /// <param name="gameBoard">Game board to use</param>
        public Game(IPlayer player1, IPlayer player2, GameBoard gameBoard)
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

        public void PerformAction(GameAction action)
        {
            GameActions.Add(action);
            action.Do();
            OnPropertyChanged("GameActions");
            OnPropertyChanged("GameLog");
        }

        internal void Reset()
        {
            Board = new GameBoard();
            PlayerTurn = RngRandom.Instance.Next(0, 1) == 0 ? Player1 : Player2;
            OnPropertyChanged("Board");
            OnPropertyChanged("GameActions");
            OnPropertyChanged("GameLog");
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
}
