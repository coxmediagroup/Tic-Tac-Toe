using System;
using System.ComponentModel;
using System.Threading;
using System.Windows;
using Common.Logging.Configuration;
using TicTacToe.Core;
using TicTacToe.Core.Actions;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    using System.Threading.Tasks;

    public class GameViewModel : DependencyObject, INotifyPropertyChanged
    {
        public Game Game
        {
            get
            {
                return this.game;
            }
            set
            {
                if (Equals(value, this.game))
                {
                    return;
                }
                this.game = value;
                this.OnPropertyChanged("Game");
            }
        }

        public string Player1Name
        {
            get
            {
                return this.player1Name;
            }
            set
            {
                if (value == this.player1Name) return;
                this.player1Name = value;
                OnPropertyChanged("Player1Name");
            }
        }

        public string Player2Name
        {
            get
            {
                return this.player2Name;
            }
            set
            {
                if (value == this.player2Name) return;
                this.player2Name = value;
                OnPropertyChanged("Player2Name");
            }
        }

        public bool IsPlayer1Turn
        {
            get
            {
                return Game.PlayerTurn == Game.Player1;
            }
        }

        public bool IsPlayer2Turn
        {
            get
            {
                return Game.PlayerTurn == Game.Player2;
            }
        }

        public bool ShowPlayerName
        {
            get
            {
                return Game.Winner != null;
            }
        }

        public int Player1WinCount
        {
            get { return _player1WinCount; }
            set
            {
                if (value == _player1WinCount) return;
                _player1WinCount = value;
                OnPropertyChanged("Player1WinCount");
            }
        }

        public int Player2WinCount
        {
            get { return _player2WinCount; }
            set
            {
                if (value == _player2WinCount) return;
                _player2WinCount = value;
                OnPropertyChanged("Player2WinCount");
            }
        }

        public int TieCount
        {
            get { return _tieCount; }
            set
            {
                if (value == _tieCount) return;
                _tieCount = value;
                OnPropertyChanged("TieCount");
            }
        }

        public static readonly DependencyProperty GameBoardViewModelProperty =
            DependencyProperty.Register("GameBoardViewModel", typeof(GameBoardViewModel), typeof(GameViewModel), new PropertyMetadata(default(GameBoardViewModel)));

        private string player1Name;

        private string player2Name;

        private Game game;
        private int _player1WinCount;
        private int _player2WinCount;
        private int _tieCount;

        public GameBoardViewModel GameBoardViewModel
        {
            get { return (GameBoardViewModel)GetValue(GameBoardViewModelProperty); }
            set { SetValue(GameBoardViewModelProperty, value); }
        }

        public GameViewModel()
        {
            Game = new Game(new HumanPlayer("Player 1"), new HumanPlayer("Player 2"));
            Player1Name = Game.Player1.Name;
            Player2Name = Game.Player2.Name;
            Game.PropertyChanged += GameOnPropertyChanged;
            GameBoardViewModel = new GameBoardViewModel(this);
            var t = new System.Timers.Timer(1000);
            t.Elapsed += (sender, args) =>
            {

            };
            t.Start();
        }

        private void GameOnPropertyChanged(object sender, PropertyChangedEventArgs args)
        {
            this.OnPropertyChanged("IsPlayer1Turn");
            this.OnPropertyChanged("IsPlayer2Turn");
            this.OnPropertyChanged("ShowPlayerName");
            if (args.PropertyName == "Status")
            {
                if (Game.Status == GameStatus.Finished)
                {
                    if (Game.Winner == Game.Player1)
                    {
                        Player1WinCount++;
                    }
                    else if (Game.Winner == Game.Player2)
                    {
                        Player2WinCount++;
                    }
                    else if (Game.WinStatus == GameWinStatus.Tie)
                    {
                        TieCount++;
                    }
                    Task.Factory.StartNew(() =>
                    {
                        var rg = new ResetGameAction(Game, Game.PlayerTurn);
                        Thread.Sleep(3000);
                        Game.PerformAction(rg);
                        Dispatcher.Invoke(new Action(() =>
                        {
                            GameBoardViewModel.Dispose();
                            GameBoardViewModel = new GameBoardViewModel(this);
                        }));
                    });
                }
            }
        }

        public void Start()
        {
            Task.Factory.StartNew(() =>
            {
                Game.Start();
            });
        }

        public void Reset(IPlayer player1, IPlayer player2)
        {
            GameBoardViewModel.Dispose();
            Game.PropertyChanged -= GameOnPropertyChanged;
			if(Game != null)
				Game.Dispose();
            Game = new Game(player1, player2);
            Game.PropertyChanged += GameOnPropertyChanged;
            GameBoardViewModel = new GameBoardViewModel(this);
            this.Player1WinCount = 0;
            this.Player2WinCount = 0;
            this.TieCount = 0;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        [NotifyPropertyChangedInvocator]
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null) handler(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}