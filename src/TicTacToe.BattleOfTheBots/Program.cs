using TicTacToe.Core;

namespace TicTacToe.BattleOfTheBots
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;

    using Common.Logging;

    using TicTacToe.Core;

    public class Program
    {
        public static ILog Log = LogManager.GetCurrentClassLogger();
        static void Main(string[] args)
        {
            Log.Info("Starting");

            var resultList = new List<RunResult>();

			var p1 = new AiPlayer("TimWinBot",GameWinStatus.Win);
            var p2 = new AiPlayer("JimTieBot",GameWinStatus.Tie);
            for (var i = 0; i < 100; i++)
            {
				var top = Console.CursorTop;
                DrawProgressBar(i, 99, '#', "");
                Console.WriteLine();
                var time = new Stopwatch();
                time.Start();
                var game = new Game(p1, p2);
                game.Start();
                time.Stop();
                //Console.WriteLine("[{0}ms]{1} - {2}",time.ElapsedMilliseconds, game.WinStatus, game.Winner);
				resultList.Add(new RunResult(game.Winner,game.WinStatus,time.ElapsedMilliseconds));
            }
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
            int barSize = Console.BufferWidth - 14;
            Console.CursorVisible = false;
            int top = Console.CursorTop;
            Console.WriteLine(message);
            int left = Console.CursorLeft;
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
            Console.CursorLeft = left;
            Console.CursorTop = top;
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
