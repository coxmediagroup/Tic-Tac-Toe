using System.ComponentModel;
using System.Windows.Controls;
using TicTacToe.Controls.ViewModels;
using TicTacToe.Core.Annotations;

namespace TicTacToe.Controls
{
    /// <summary>
    /// Interaction logic for Position.xaml
    /// </summary>
    public partial class Position : INotifyPropertyChanged
    {
        private PositionViewModel _vm;

        public PositionViewModel Vm
        {
            get { return _vm; }
            set
            {
                if (Equals(value, _vm)) return;
                _vm = value;
                OnPropertyChanged("Vm");
            }
        }

        public Position()
        {
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
