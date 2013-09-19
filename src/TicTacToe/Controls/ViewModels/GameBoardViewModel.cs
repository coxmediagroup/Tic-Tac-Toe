using System.Collections.ObjectModel;
using System.ComponentModel;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls.ViewModels
{
    public class GameBoardViewModel : INotifyPropertyChanged
    {
        public ObservableCollection<PositionViewModel> Positions { get; set; }
        public GameViewModel GameVm { get; set; }

        public GameBoardViewModel(GameViewModel gameVm)
        {
            GameVm = gameVm;
            Positions = new ObservableCollection<PositionViewModel>();
            for(var y = 0;y<3;y++)
            {
                for(var x = 0;x<3;x++)
                {
                    var np = new PositionViewModel(x, y, GameVm.Game.Board.BoardPositions[y][x], GameVm);
                    Positions.Add(np);
                }
            }
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