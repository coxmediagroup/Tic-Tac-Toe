using System;
using System.ComponentModel;
using TicTacToe.Core;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    public class GameViewModel : INotifyPropertyChanged
    {
        public Game Game { get; set; }

        public GameViewModel()
        {
            Game = new Game(new HumanPlayer("Player 1"), new HumanPlayer("Player 2"));
            Game.PropertyChanged += GameOnPropertyChanged;
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