namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.Globalization;
    using System.IO;
    using System.Linq;

    using Common.Logging;

    using TicTacToe.Core.Actions;
    using TicTacToe.Core.Utils;

    public class LearnProcessor
    {
        internal static object FileLock = new Object();
        internal static ILog Log = LogManager.GetCurrentClassLogger();
        internal static int[] AllSpaces = new int[9] { 0, 1, 2, 3, 4, 5, 6, 7, 8 };

        internal string LearnFile { get; set; }

        internal List<long> CacheList { get; set; }

        public int LearnCount
        {
            get
            {
                lock (FileLock) return CacheList.Count;
            }
        }

        public LearnProcessor(string learnFile)
        {
            lock (FileLock)
            {
                LearnFile = learnFile;
                if (!File.Exists(LearnFile)) File.Create(LearnFile).Close();
                CacheList = File.ReadAllLines(LearnFile).Select(long.Parse).ToList();
            }
        }

        public void ProcessEndGame(Game game)
        {
            if (game.Status != GameStatus.Finished)
                throw new InvalidOperationException("Game must be finished before processing");

            if (game.WinStatus == GameWinStatus.None)
                throw new InvalidOperationException("Game win status must be set before processing");

            var state = new GameState(game);
            if (CacheList.Contains(GameState.ToLong(state)))
            {
                //Log.Debug("State already exists");
                return;
            }
            lock (FileLock)
            {
                File.AppendAllLines(LearnFile, new[] { GameState.ToLong(state).ToString(CultureInfo.InvariantCulture) });
                CacheList.Add(GameState.ToLong(state));
            }
        }

        /// <summary>
        /// Get the next move
        /// </summary>
        /// <param name="player">The player requesting a move</param>
        /// <param name="game">Game being played</param>
        /// <param name="learning">Are we learning moves</param>
        /// <returns></returns>
        public int GetNextMove(IPlayer player, Game game, bool learning)
        {
            IPlayer firstPlayer = null;
            var firstOccupy = game.GameActions.OfType<OccupyGameAction>().FirstOrDefault();
            firstPlayer = firstOccupy != null ? firstOccupy.Player : game.PlayerTurn;
			
            var otherPlayer = game.Player1 == firstPlayer ? game.Player2 : game.Player1;
            var gameStates = CacheList.Select(x => GameState.FromLong(x, firstPlayer, otherPlayer)).ToArray();

            var moveList = MoveListFromGame(game);

            // If we're learning, then don't use any states that we have saved
            if (learning)
            {
				var availableMoves = AllSpaces
					.Where(x => moveList.Any(y => y.Move == x) == false)
					.Select(x => new MoveItem(x, player))
					.ToList();
				// Try and make a move that hasn't been stored yet.
                foreach (var m in availableMoves)
                {
                    moveList.Add(m);
                    if (gameStates.Any(x => x.Contains(moveList)) == false)
                    {
                        return m.Move;
                    }
                    moveList.Remove(m);
                }
				// Every variation of the next move has been stored, drop down to brain mode
                var ret = RngRandom.Instance.Next(0, availableMoves.Count);
                return availableMoves[ret].Move;
            }

            var allMoves = gameStates
                .Where(x => x.Contains(moveList)) //Only grab states that we can use
                .OrderByDescending(x => x.WinStatus)
                .ToArray();

            var nonLosingMoves = allMoves
                .Where(x => x.Winner == player || x.Winner == null)// Only grab ties or ones where we win
                .ToArray();

            var nextMove = nonLosingMoves.FirstOrDefault();
            if (nextMove != null)
            {
                return nextMove.MoveList.Skip(moveList.Count).Take(1).First().Move;
            }

            nextMove = allMoves.First();
            return nextMove.MoveList.Skip(moveList.Count).Take(1).First().Move;
        }

        internal List<MoveItem> MoveListFromGame(Game game)
        {
            return game.GameActions
                .OfType<OccupyGameAction>()
                .Select(x => new MoveItem((x.Y * 3) + x.X, x.Player))
                .ToList();
        }
    }
}