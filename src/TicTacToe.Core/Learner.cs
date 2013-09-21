namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.Globalization;
    using System.IO;
    using System.Linq;

    using Common.Logging;

    using TicTacToe.Core.Actions;

    public class LearnProcessor
    {
        internal static ILog Log = LogManager.GetCurrentClassLogger();

		internal string LearnFile { get; set; }

		internal List<long> CacheList { get; set; }

        public LearnProcessor(string learnFile)
        {
            LearnFile = LearnFile;
            if (!File.Exists(learnFile))
                File.Create(LearnFile).Close();
            CacheList = File.ReadAllLines(LearnFile).Select(long.Parse).ToList();
        }

        public void ProcessEndGame(Game game)
        {
            if (game.Status != GameStatus.Finished) 
                throw new InvalidOperationException("Game must be finished before processing");

			if(game.WinStatus == GameWinStatus.None)
				throw new InvalidOperationException("Game win status must be set before processing");

            var state = BoardToLong(game);
            if (CacheList.Contains(state))
            {
                Log.Debug("State already exists");
                return;
            }
            File.AppendAllLines(LearnFile, new[] { state.ToString(CultureInfo.InvariantCulture) });
			CacheList.Add(state);
        }

        internal long BoardToLong(Game game)
        {
            long boardState = 0;
            var moveList = game.GameActions.OfType<OccupyGameAction>().ToArray();
            var startPlayer = moveList.First().Player;
            var skip = 0;
            byte pbyte = 1;
            foreach (var m in moveList)
            {
				// Index + 1
                var idx = (byte)((((m.Y * 3) + m.X) + 1) & 0x0F);
                // Empty = 1, StartPlayer = 2, OtherPlayer = 3
                if (m.Player == startPlayer) pbyte = 2;
                else if (m.Player != null) pbyte = 3;

				// 4 bits
                boardState = (boardState << skip) | idx;

                skip = 2;

				// 2 bits
                boardState = (boardState << skip) | (pbyte & 0x03);

                skip = 4;

            }
			// Winning player
			// 1 == No one(tie)
			// 2 == Starting Player
			// 3 == Other Player
            pbyte = 1;
            if (game.Winner == startPlayer) pbyte = 2;
            else if (game.Winner != null) pbyte = 3;
            boardState = (boardState << 2) | (pbyte & 0x03);

            return boardState;
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
			// If we're learning, then don't use any states that we have saved
            if (learning)
            {

                return 0;
            }

            return 0;
        }
    }
}