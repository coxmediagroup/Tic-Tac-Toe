using System.ComponentModel;
using System.Windows;
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
        public static readonly DependencyProperty VmProperty =
            DependencyProperty.Register("Vm", typeof (PositionViewModel), typeof (Position), new PropertyMetadata(default(PositionViewModel)));

        public PositionViewModel Vm
        {
            get { return (PositionViewModel) GetValue(VmProperty); }
            set { SetValue(VmProperty, value); }
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
