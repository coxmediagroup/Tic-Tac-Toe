using System.ComponentModel;
using TicTacToe.Core;
using TicTacToe.Core.Players;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    using System;

    using Core.Actions;

    public class PositionViewModel : INotifyPropertyChanged, IDisposable
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
		internal bool WasSet { get; set; }

        public PositionViewModel(int x, int y, IPlayer player, GameViewModel gameVm)
        {
            Player = player;
            X = x;
            Y = y;
            GameVm = gameVm;
			GameVm.Game.Board.OnOccupy += BoardOnOnOccupy;
        }

        private void BoardOnOnOccupy(IPlayer player, int x, int y)
        {
            if (x == X && y == Y)
				Player = player;
        }

        public void HandleClick()
        {
            if (GameVm.Game.Status == GameStatus.Finished) return;
            if (GameVm.Game.WinStatus != GameWinStatus.None) return;
            if (GameVm.Game.PlayerTurn is AiPlayer) return;
            if (GameVm.Game.Board.IsPositionOccupied(X, Y))
                return;
			var action = new OccupyGameAction(GameVm.Game,GameVm.Game.PlayerTurn,X,Y,0);
			GameVm.Game.PerformAction(action);
        }

        public event PropertyChangedEventHandler PropertyChanged;

        [NotifyPropertyChangedInvocator]
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null) handler(this, new PropertyChangedEventArgs(propertyName));
        }

        public void Dispose()
        {
            GameVm.Game.Board.OnOccupy -= BoardOnOnOccupy;
        }
    }
}