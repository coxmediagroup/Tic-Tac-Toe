using System;
using System.Collections.Generic;
using System.Linq;
using TicTacToe.Core.Actions;

namespace TicTacToe.Core.Players.AI
{
    public class GameState
    {
        internal static Dictionary<long, GameState> GameStateCache = new Dictionary<long, GameState>();

        public int MoveCount { get; set; }
        public IPlayer Player1 { get; set; }
        public IPlayer Player2 { get; set; }
        public IPlayer Winner { get; set; }
        public List<MoveItem> MoveList { get; set; }

        public List<List<MoveItem>> AllTransforms { get; set; }

        public GameWinStatus WinStatus
        {
            get
            {
                return Winner == null ? GameWinStatus.Tie : GameWinStatus.Win;
            }
        }

        public GameState()
        {
            this.MoveList = new List<MoveItem>();
        }

        public GameState(Game game)
        {
            if (game.Status != GameStatus.Finished)
                throw new InvalidOperationException("Game must be finished before processing");

            if (game.WinStatus == GameWinStatus.None)
                throw new InvalidOperationException("Game win status must be set before processing");

            this.MoveList = game.GameActions.OfType<OccupyGameAction>().Select(x => new MoveItem((x.Y * 3) + x.X, x.Player)).ToList();

            this.MoveCount = this.MoveList.Count;

            this.Player1 = game.StartPlayer;
            this.Player2 = game.Player1 == this.Player1 ? game.Player2 : game.Player1;

            this.Winner = game.Winner;

            AllTransforms = GetTransforms(MoveList).ToList();
        }

        public bool Contains(List<MoveItem> moveList)
        {
            foreach (var tran in AllTransforms)
            {
                var match = false;
                if (tran[0].Move != moveList[0].Move)
                {
                    match = false;
                    continue;
                }
                for (var i = 0; i < moveList.Count; i++)
                {
                    if (tran[i].Equals(moveList[i]))
                    {
                        match = true;
                    }
                    else
                    {
                        match = false;
                        break;
                    }
                }
                if (match)
                {
                    return true;
                }
            }
            return false;
            foreach (var tran in GetTransforms(MoveList))
            {
                var match = false;
                for (var i = 0; i < moveList.Count; i++)
                {
                    if (tran[i].Equals(moveList[i]))
                    {
                        match = true;
                    }
                    else
                    {
                        match = false;
                        break;
                    }
                }
                if (match)
                {
                    return true;
                }
            }
            return false;
        }

        public MoveItem NextMove(List<MoveItem> moves)
        {
            foreach (var tran in GetTransforms(MoveList))
            {
                var match = false;
                for (var i = 0; i < moves.Count; i++)
                {
                    if (tran[i].Equals(moves[i]))
                    {
                        match = true;
                    }
                    else
                    {
                        match = false;
                        break;
                    }
                }
                if (match)
                {
                    // Got our local transformation.
                    var ret = tran.Skip(moves.Count).Take(1).First();
                    return ret;
                }
            }
            return null;
        }

        public static long[] ToLongs(GameState gameState)
        {
            var gs = gameState.MemberwiseClone() as GameState;
            var ret = new List<long>();
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.FlipHorizontally());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.FlipHorizontally());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());

            // Now invert the players
            var p1 = gs.Player2;
            var p2 = gs.Player1;
            gs.Player1 = p1;
            gs.Player2 = p2;

            if (gs.Winner != null)
            {
                gs.Winner = gs.Winner == gs.Player1 ? gs.Player2 : gs.Player1;
            }

            gs.MoveList.ForEach(x => x.Player = x.Player == gs.Player1 ? gs.Player2 : gs.Player1);

            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.FlipHorizontally());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.FlipHorizontally());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());
            ret.Add(ToLong(gs));
            gs.MoveList.ForEach(x => x.RotateLeft());

            // Now put the players back the way they were

            p1 = gs.Player2;
            p2 = gs.Player1;
            gs.Player1 = p1;
            gs.Player2 = p2;

            if (gs.Winner != null)
            {
                gs.Winner = gs.Winner == gs.Player1 ? gs.Player2 : gs.Player1;
            }

            gs.MoveList.ForEach(x => x.Player = x.Player == gs.Player1 ? gs.Player2 : gs.Player1);

            return ret.ToArray();
        }

        public IEnumerable<List<MoveItem>> GetTransforms(List<MoveItem> moveList)
        {
            var m2 = moveList.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.FlipHorizontally());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.FlipHorizontally());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());

            // Now invert the players
            var p1 = moveList[0].Player;
            var p2 = moveList[1].Player;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.Player = x.Player == p1 ? p2 : p1);

            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.FlipHorizontally());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.FlipHorizontally());
            yield return m2;
            m2 = m2.Select(x => new MoveItem(x.Move, x.Player)).ToList();
            m2.ForEach(x => x.RotateLeft());
            yield return m2;
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
            GameState ret = null;
            if (GameStateCache.ContainsKey(gameState))
            {
                ret = GameStateCache[gameState];
                ret.Player1 = startPlayer;
                ret.Player2 = player2;
                return ret;
            }

            var state = gameState;
            ret = new GameState();
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
            ret.AllTransforms = ret.GetTransforms(ret.MoveList).ToList();
            GameStateCache.Add(gameState, ret);

            return ret;
        }
    }
}