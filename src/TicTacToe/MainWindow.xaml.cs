using System;
using System.ComponentModel;
using System.Windows;
using TicTacToe.Controls.ViewModels;
using TicTacToe.Core.Annotations;

namespace TicTacToe
{
    using System.Windows.Input;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : INotifyPropertyChanged
    {
        private GameViewModel _vm;

        private bool setupVisible;

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

        public bool SetupVisible
        {
            get
            {
                return this.setupVisible;
            }
            set
            {
                if (value.Equals(this.setupVisible))
                {
                    return;
                }
                this.setupVisible = value;
                this.OnPropertyChanged("SetupVisible");
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

        private void OnSetupClick(object sender, MouseButtonEventArgs e)
        {
            SetupVisible = SetupVisible == false;
        }
    }
}
