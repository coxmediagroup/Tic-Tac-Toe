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

			var p1 = new AiPlayer("TimBot");
            var p2 = new AiPlayer("JimBot");
            for (var i = 0; i < 100; i++)
            {
                var time = new Stopwatch();
                time.Start();
                var game = new Game(p1, p2);
                game.Start();
                time.Stop();
                Console.WriteLine("[{0}ms]{1} - {2}",time.ElapsedMilliseconds, game.WinStatus, game.Winner);
				resultList.Add(new RunResult(game.Winner,game.WinStatus,time.ElapsedMilliseconds));
            }
            Log.Info("Stopping");
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
