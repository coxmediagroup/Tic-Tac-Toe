using System.ComponentModel;
using TicTacToe.Core;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    public class PositionViewModel : INotifyPropertyChanged
    {
        private IPlayer _player;

        public IPlayer Player
        {
            get { return _player; }
            set
            {
                if (Equals(value, _player)) return;
                _player = value;
                OnPropertyChanged("Player");
                OnPropertyChanged("ShowX");
                OnPropertyChanged("ShowO");
            }
        }

        public bool ShowX
        {
            get
            {
                if (Player == GameVm.Game.Player1)
                    return true;
                return false;
            }
        }

        public bool ShowO
        {
            get
            {
                if (Player == GameVm.Game.Player2)
                    return true;
                return false;
            }
        }

        public int X { get; set; }
        public int Y { get; set; }
        public GameViewModel GameVm { get; set; }

        public PositionViewModel(int x, int y, IPlayer player, GameViewModel gameVm)
        {
            Player = player;
            X = x;
            Y = y;
            GameVm = gameVm;
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