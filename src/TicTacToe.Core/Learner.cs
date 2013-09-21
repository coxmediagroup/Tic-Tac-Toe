namespace TicTacToe.Core
{
    using System;
    using System.Linq;

    using TicTacToe.Core.Actions;

    public class LearnProcessor
    {
        public void Process(string learnFile, Game game)
        {
            if (game.Status != GameStatus.Finished) 
                throw new InvalidOperationException("Game must be finished before processing");

			if(game.WinStatus == GameWinStatus.None)
				throw new InvalidOperationException("Game win status must be set before processing");

            var state = BoardToLong(game);
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

                boardState = (boardState << skip) | idx;

                skip = 2;

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
    }
}