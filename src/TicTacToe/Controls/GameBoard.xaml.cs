using System.ComponentModel;
using System.Windows;
using TicTacToe.Controls.ViewModels;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls
{
    /// <summary>
    /// Interaction logic for GameBoard.xaml
    /// </summary>
    public partial class GameBoard : INotifyPropertyChanged
    {
        public static readonly DependencyProperty VmProperty =
            DependencyProperty.Register("Vm", typeof (GameBoardViewModel), typeof (GameBoard), new PropertyMetadata(default(GameBoardViewModel)));

        public GameBoardViewModel Vm
        {
            get { return (GameBoardViewModel) GetValue(VmProperty); }
            set { SetValue(VmProperty, value); }
        }
        public GameBoard()
        {
            InitializeComponent();
        }

        public GameBoard(GameBoardViewModel vm)
        {
            Vm = vm;
            InitializeComponent();   
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
