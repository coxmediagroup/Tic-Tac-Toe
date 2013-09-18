using System;
using System.Windows;

namespace TicTacToe
{
    using log4net;

    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            GlobalContext.Properties["version"] = typeof(App).Assembly.GetName().Version;
            GlobalContext.Properties["os"] = Environment.OSVersion.ToString();
            base.OnStartup(e);
        }
    }
}
