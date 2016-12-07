namespace TicTacToe
{
    using System;
    using System.Globalization;
    using System.Windows;
    using System.Windows.Data;
    using System.Windows.Media;

    using Core;

    [ValueConversion(typeof(bool), typeof(Visibility))]
    public class InvertedBooleanToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var val = (bool)value;
            return val ? Visibility.Collapsed : Visibility.Visible;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

	[ValueConversion(typeof(GameWinStatus),typeof(Brush))]
    public class WinStatusToColorConverter : IValueConverter
	{
	    public static SolidColorBrush WinBrush = new SolidColorBrush(Colors.Green);
	    public static SolidColorBrush TieBrush = new SolidColorBrush(Colors.Gray);
	    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
	    {
	        var status = (GameWinStatus)value;
	        switch (status)
	        {
	            case GameWinStatus.Win:
	                return WinBrush;
	            default:
	                return TieBrush;
	        }
	    }

	    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
	    {
	        throw new NotImplementedException();
	    }
    }

    [ValueConversion(typeof(GameStatus), typeof(Visibility))]
    public class GameStatusToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var status = (GameStatus)value;
            switch (status)
            {
                case GameStatus.Finished:
                    return Visibility.Visible;
                default:
                    return Visibility.Collapsed;
            }
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}