using TicTacToe.Core;

namespace TicTacToe.BattleOfTheBots
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Threading;
	using System.Linq;

    using Common.Logging;

    using TicTacToe.Core;

    public class Program
    {
        public static ILog Log = LogManager.GetCurrentClassLogger();

        public static int Left;
        public static int Top;

        public static List<RunResult> ResultList = new List<RunResult>();

        static void Main(string[] args)
        {
            Log.Info("Starting");

            ResultList = new List<RunResult>();

			var p1 = new AiPlayer("TimWinBot",GameWinStatus.Win);
            var p2 = new AiPlayer("JimTieBot",GameWinStatus.Tie);
            var maxCount = 1000000;
            Console.CursorTop = 3;
            for (var i = 0; i < maxCount; i++)
            {
                DrawProgressBar(i, maxCount - 1, '#', "");
                var time = new Stopwatch();
                time.Start();
                var game = new Game(p1, p2);
                game.Start();
                Thread.Sleep(10);
                time.Stop();
                var oldColor = Console.ForegroundColor;
                if (game.WinStatus == GameWinStatus.Win)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("[{0}ms] {1} - {2}", time.ElapsedMilliseconds, game.WinStatus, game.Winner);
                    Console.ForegroundColor = oldColor;
                }
				ResultList.Add(new RunResult(game.Winner, game.WinStatus, time.ElapsedMilliseconds));
            }
			Console.SetCursorPosition((Console.WindowWidth / 2) - 2,Console.WindowHeight - 2);
            Console.WriteLine("Done");
            Console.ReadKey();
            Log.Info("Stopping");
        }

		/// <summary>
		/// Draws a progress bar on the screen.
		/// Took this from another open source project I have https://github.com/kellyelton/ShuffleValidator/blob/master/src/ShuffleValidator/Program.cs#L121
		/// </summary>
		/// <param name="complete"></param>
		/// <param name="maxVal"></param>
		/// <param name="progressCharacter"></param>
		/// <param name="message"></param>
		private static void DrawProgressBar(int complete, int maxVal, char progressCharacter, string message)
        {
            Top = Console.CursorTop;
            Console.SetCursorPosition(0, 0);
            int barSize = Console.BufferWidth - 14;
            Console.CursorVisible = false;
            Console.WriteLine(message);
            decimal perc = (decimal)complete / (decimal)maxVal;
            int chars = (int)Math.Floor(perc / ((decimal)1 / (decimal)barSize));
            string p1 = String.Empty, p2 = String.Empty;

            for (int i = 0; i < chars; i++) p1 += progressCharacter;
            for (int i = 0; i < barSize - chars; i++) p2 += progressCharacter;

            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write(p1);
            Console.ForegroundColor = ConsoleColor.DarkGreen;
            Console.Write(p2);
            
            Console.ResetColor();
            Console.Write(" {0}%", (perc * 100).ToString("N2"));
		    Console.CursorLeft = 0;
		    ShowStatsBar();
            Console.CursorLeft = Left;
            Console.CursorTop = Top;
            if (Top == Console.WindowHeight - 3)
            {
                Left += 26;
                if (Left >= Console.WindowWidth - 26) 
                    Left = 0;
                Top = 3;
                Console.CursorLeft = Left;
                Console.CursorTop = Top;
            }
            Console.SetCursorPosition(Console.CursorLeft, Console.CursorTop);
        }

        private static void ShowStatsBar()
        {
            Console.CursorTop++;
			for(var i = 0;i<Console.BufferWidth;i++)
				Console.Write(" ");
            Console.CursorTop--;
            if (ResultList.Count == 0) return;
            var wins = ResultList.Count(x => x.Status == GameWinStatus.Win);
            var ties = ResultList.Count(x => x.Status == GameWinStatus.Tie);
            var avgtime = ResultList.Average(x => x.Milliseconds);
            var mostwins = ResultList.GroupBy(x => x.Winner).Select(x => new { Wins = x.Count(), Player = x.First().Winner }).OrderByDescending(x=>x.Wins).ToArray();
            var str = string.Format("Wins: {0}     Ties: {1}    AvgTime: {2}    MostWins: {3}", wins, ties, (int)avgtime, mostwins.First().Player);
            Console.CursorLeft = (Console.WindowWidth / 2) - (str.Length / 2);
            Console.Write(str);
        }
    }

    public class RunResult
    {
        public IPlayer Winner { get; set; }
		public GameWinStatus Status { get; set; }
		public long Milliseconds { get; set; }

        public RunResult(IPlayer winner, GameWinStatus status, long milliseconds)
        {
            Winner = winner;
            Status = status;
            Milliseconds = milliseconds;
        }
    }
}
