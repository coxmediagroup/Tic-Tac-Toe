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
        internal static int[] AllSpaces = new int[9] { 0, 1, 2, 3, 4, 5, 6, 7, 8 };

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

            if (game.WinStatus == GameWinStatus.None)
                throw new InvalidOperationException("Game win status must be set before processing");

            var state = new GameState(game);
            if (CacheList.Contains(GameState.ToLong(state)))
            {
                Log.Debug("State already exists");
                return;
            }
            File.AppendAllLines(LearnFile, new[] { GameState.ToLong(state).ToString(CultureInfo.InvariantCulture) });
            CacheList.Add(GameState.ToLong(state));
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
            }

            var allMoves = gameStates
                .Where(x => x.Contains(moveList)) //Only grab states that we can use
                .OrderBy(x => x.Winner == null)
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

    public class GameState
    {
        public int MoveCount { get; set; }
        public IPlayer Player1 { get; set; }
        public IPlayer Player2 { get; set; }
        public IPlayer Winner { get; set; }
        public List<MoveItem> MoveList { get; set; }

        public GameState()
        {
            MoveList = new List<MoveItem>();
        }

        public GameState(Game game)
        {
            if (game.Status != GameStatus.Finished)
                throw new InvalidOperationException("Game must be finished before processing");

            if (game.WinStatus == GameWinStatus.None)
                throw new InvalidOperationException("Game win status must be set before processing");

            MoveList = game.GameActions.OfType<OccupyGameAction>().Select(x => new MoveItem((x.Y * 3) + x.X, x.Player)).ToList();

            MoveCount = MoveList.Count;

            Player1 = MoveList.First().Player;
            Player2 = MoveList.First(x => x.Player != Player1).Player;

            Winner = game.Winner;
        }

        public bool Contains(List<MoveItem> moveList)
        {
            return !moveList.Where((t, i) => !t.Equals(this.MoveList[i])).Any();
        }

        /// <summary>
        /// Converts a GameState to a long
        /// </summary>
        /// <param name="gameState">The GameState to convert</param>
        /// <returns>long value representing the GameState</returns>
        public static long ToLong(GameState gameState)
        {
            long boardState = 0;
            var skip = 0;
            byte pbyte = 1;
            foreach (var m in gameState.MoveList)
            {
                // Index + 1
                var idx = (byte)(((m.Move) + 1) & 0x0F);
                // Empty = 1, StartPlayer = 2, OtherPlayer = 3
                if (m.Player == gameState.Player1) pbyte = 2;
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
            if (gameState.Winner == gameState.Player1) pbyte = 2;
            else if (gameState.Winner != null) pbyte = 3;
            boardState = (boardState << 2) | (pbyte & 0x03);

            // Append on the number of moves
            var mnum = (byte)(gameState.MoveCount & 0x0F);
            boardState = (boardState << 4) | mnum;

            return boardState;
        }

        /// <summary>
        /// Converts a long to a GameState
        /// </summary>
        /// <param name="gameState">long that contains state</param>
        /// <param name="startPlayer">The player that started the current game</param>
        /// <param name="player2">The other player</param>
        /// <returns>GameState contained in long</returns>
        public static GameState FromLong(long gameState, IPlayer startPlayer, IPlayer player2)
        {
            var state = gameState;
            var ret = new GameState();
            ret.Player1 = startPlayer;
            ret.Player2 = player2;

            // Get the move count
            ret.MoveCount = (int)(state & 0x0F);

            state >>= 4; //Remove movecount from state

            // Get the winning player
            switch ((byte)(state & 0x03))
            {
                case 2:
                    ret.Winner = startPlayer;
                    break;
                case 3:
                    ret.Winner = player2;
                    break;
            }

            state >>= 2; // Remove winning player from state

            // Get all the moves
            for (var i = 0; i < ret.MoveCount; i++)
            {
                // Player
                var pbyte = ((byte)(state & 0x03));

                state >>= 2; // Remove player from state

                var move = ((byte)(state & 0x0F));

                state >>= 4; // Remove move nibble from state

                IPlayer player = null;
                switch (pbyte)
                {
                    case 2:
                        player = startPlayer;
                        break;
                    case 3:
                        player = player2;
                        break;
                }
                ret.MoveList.Add(new MoveItem(move - 1, player));
            }
            ret.MoveList.Reverse();

            return ret;
        }
    }

    public class MoveItem : IEquatable<MoveItem>
    {
        public int Move { get; set; }
        public IPlayer Player { get; set; }

        public MoveItem(int move, IPlayer player)
        {
            Move = move;
            Player = player;
        }

        public bool Equals(MoveItem other)
        {
            return this.Move == other.Move && this.Player == other.Player;
        }
    }
}