using System;
using System.ComponentModel;
using System.Windows;
using TicTacToe.Core;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    public class GameViewModel : DependencyObject
    {
        public Game Game { get; set; }

        public static readonly DependencyProperty GameBoardViewModelProperty =
            DependencyProperty.Register("GameBoardViewModel", typeof (GameBoardViewModel), typeof (GameViewModel), new PropertyMetadata(default(GameBoardViewModel)));

        public GameBoardViewModel GameBoardViewModel
        {
            get { return (GameBoardViewModel) GetValue(GameBoardViewModelProperty); }
            set { SetValue(GameBoardViewModelProperty, value); }
        }

        public GameViewModel()
        {
            Game = new Game(new HumanPlayer("Player 1"), new HumanPlayer("Player 2"));
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