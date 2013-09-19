using System.ComponentModel;
using TicTacToe.Core;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    public class GameViewModel : INotifyPropertyChanged
    {
        private IPlayer _xPlayer;
        private IPlayer _oPlayer;

        public IPlayer XPlayer
        {
            get { return _xPlayer; }
            set
            {
                if (Equals(value, _xPlayer)) return;
                _xPlayer = value;
                OnPropertyChanged("XPlayer");
            }
        }

        public IPlayer OPlayer
        {
            get { return _oPlayer; }
            set
            {
                if (Equals(value, _oPlayer)) return;
                _oPlayer = value;
                OnPropertyChanged("OPlayer");
            }
        }

        public Game Game { get; set; }

        public GameViewModel()
        {
            XPlayer = new HumanPlayer("Player 1");
            OPlayer = new HumanPlayer("Player 2");
            Game = new Game(XPlayer, OPlayer);
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