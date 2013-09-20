using System;
using System.ComponentModel;
using System.Windows;
using TicTacToe.Core;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
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

        public static readonly DependencyProperty GameBoardViewModelProperty =
            DependencyProperty.Register("GameBoardViewModel", typeof (GameBoardViewModel), typeof (GameViewModel), new PropertyMetadata(default(GameBoardViewModel)));

        private string player1Name;

        private string player2Name;

        private Game game;

        public GameBoardViewModel GameBoardViewModel
        {
            get { return (GameBoardViewModel) GetValue(GameBoardViewModelProperty); }
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

        private void GameOnPropertyChanged(object sender, PropertyChangedEventArgs propertyChangedEventArgs)
        {
        }

        public void Start()
        {
            Game.Start();
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