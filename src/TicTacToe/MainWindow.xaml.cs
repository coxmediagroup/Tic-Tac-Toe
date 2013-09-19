using System;
using System.ComponentModel;
using System.Windows;
using TicTacToe.Controls.ViewModels;
using TicTacToe.Core.Annotations;

namespace TicTacToe
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : INotifyPropertyChanged
    {
        private GameViewModel _vm;

        public GameViewModel Vm
        {
            get { return _vm; }
            set
            {
                if (Equals(value, _vm)) return;
                _vm = value;
                OnPropertyChanged("Vm");
            }
        }

        public MainWindow()
        {
            InitializeComponent();
            this.Loaded += OnLoaded;
        }

        private void OnLoaded(object sender, RoutedEventArgs routedEventArgs)
        {
            this.Loaded -= OnLoaded;
            Vm = new GameViewModel();
            Vm.Start();
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
