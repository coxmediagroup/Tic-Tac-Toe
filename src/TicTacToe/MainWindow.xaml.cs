using System;
using System.ComponentModel;
using System.Windows;
using TicTacToe.Controls.ViewModels;
using TicTacToe.Core.Annotations;

namespace TicTacToe
{
    using System.Windows.Input;

    using TicTacToe.Core;

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
            SetupVisible = true;
        }

        private void OnCancelClick(object sender, MouseButtonEventArgs e)
        {
            Vm.Player1Name = Vm.Game.Player1.Name;
            Vm.Player2Name = Vm.Game.Player2.Name;
            SetupVisible = false;
        }

        private void OnStartGameClick(object sender, MouseButtonEventArgs e)
        {
            IPlayer player1;
            IPlayer player2;
            bool hasHuman = false;

            if (String.IsNullOrWhiteSpace(Vm.Player1Name))
            {
                MessageBox.Show("X Player must have a name", "Error", MessageBoxButton.OK, MessageBoxImage.Exclamation);
                return;
            }

            if (String.IsNullOrWhiteSpace(Vm.Player2Name))
            {
                MessageBox.Show("O Player must have a name", "Error", MessageBoxButton.OK, MessageBoxImage.Exclamation);
                return;
            }

            if (Player1Type.Text == "AI")
            {
                player1 = new AiPlayer(Vm.Player1Name,true , 400);
            }
			else
            {
                Player1Type.Text = "Human";
                player1 = new HumanPlayer(Vm.Player1Name);
                hasHuman = true;
            }
            if (Player2Type.Text == "AI")
            {
                player2 = new AiPlayer(Vm.Player2Name, true, 400);
            }
			else
            {
                Player2Type.Text = "Human";
                player2 = new HumanPlayer(Vm.Player2Name);
                hasHuman = true;
            }
			Vm.Reset(player1,player2);
            if (!hasHuman)
            {
                (Vm.Game.Player1 as AiPlayer).TurnDelay = 800;
                (Vm.Game.Player2 as AiPlayer).TurnDelay = 800;
            }
            Vm.Player1Name = player1.Name;
            Vm.Player2Name = player2.Name;
            SetupVisible = false;
			Vm.Start();
        }

        private void OnResetClick(object sender, MouseButtonEventArgs e)
        {
            Vm.Reset(Vm.Game.Player1, Vm.Game.Player2);
            Vm.Start();
        }
    }
}
