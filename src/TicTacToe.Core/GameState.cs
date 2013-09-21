namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    using TicTacToe.Core.Actions;

    public class GameState
    {
        public int MoveCount { get; set; }
        public IPlayer Player1 { get; set; }
        public IPlayer Player2 { get; set; }
        public IPlayer Winner { get; set; }
        public List<MoveItem> MoveList { get; set; }

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

            this.Player1 = this.MoveList.First().Player;
            this.Player2 = this.MoveList.First(x => x.Player != this.Player1).Player;

            this.Winner = game.Winner;
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
}