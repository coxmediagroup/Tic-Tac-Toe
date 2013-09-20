using System.Linq.Expressions;
using System.Security.Cryptography.X509Certificates;
using System.Xaml;

namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;

    using TicTacToe.Core.Actions;
    using TicTacToe.Core.Utils;

    public class AiPlayer : IPlayer
    {
        public string Name { get; internal set; }
		public GameWinStatus Focus { get; internal set; }
		public int TurnDelay { get; set; }

        /// <summary>
        /// Create a <see cref="AiPlayer"/>
        /// </summary>
        /// <param name="name">Name of the <see cref="AiPlayer"/></param>
        /// <param name="focus">Choose what the Ai is more focused on achieving</param>
        /// <param name="turnDelay">Time to wait before switching the turn in ms(Default: 0)</param>
        public AiPlayer(string name, GameWinStatus focus, int turnDelay = 0)
        {
            this.Name = name;
            this.Focus = focus;
            this.TurnDelay = turnDelay;
        }

        /// <summary>
        /// Gets invoked when it's the <cref see="AiPlayer"/>'s turn.
        /// </summary>
        /// <param name="state">State of the game</param>
        public void OnTurn(Game state)
        {
            // If board is empty, then we're going first, so pick the middle one always
            if (state.Board.IsEmpty())
            {
				// For testing sakes, we're going to pick a random location
				//   for now
                var xx = RngRandom.Instance.Next(0, 3);
                var yy = RngRandom.Instance.Next(0, 3);
                var a = new OccupyGameAction(state, this, xx, yy,TurnDelay);
				state.PerformAction(a);
                return;
            }

			// Otherwise, things get a bit sticky here.
			// I suppose we can brute force this sucker and see
			//    how long it takes first.

            var result = new PlayItOutResults(this, state.Board, state, this.Focus);
            var nextMove = result.NextMove();
            int x, y;
			state.Board.IndexToCoords(nextMove,out x,out y);
            var act = new OccupyGameAction(state, this, x, y, TurnDelay);
            state.PerformAction(act);
        }

        public override string ToString()
        {
            return Name;
        }

        internal class PlayItOutResults
        {
			public int StartIndex { get; internal set; }
			public int Index { get; internal set; }
            public List<PlayItOutResults> Moves { get; internal set; }
			public GameWinStatus Status { get; internal set; }
			public IPlayer WinPlayer { get; internal set; }
			public IPlayer Me { get; internal set; }
			public Game Game { get; set; }
			public bool IsLoss { get; set; }
			public GameWinStatus Focus { get; set; }
			public int MoveCount { get; set; }

            public PlayItOutResults(IPlayer movePlayer, GameBoard board, Game game, GameWinStatus focus)
            {
                Focus = focus;
                Me = movePlayer;
                Game = game;
                Index = -1;
                Moves = new List<PlayItOutResults>();
                for (var i = 0; i < 9; i++)
                {
                    if (!board.IsPositionOccupied(i))
                    {
                        var res = new PlayItOutResults(i,i, Me, movePlayer, board, game, Focus, MoveCount);
						Moves.Add(res);
                    }
                }
            }

            public PlayItOutResults(int startIdx, int idx, IPlayer me, IPlayer movePlayer, GameBoard board, Game game, GameWinStatus focus, int moveCount)
            {
                this.MoveCount = moveCount;
                Focus = focus;
                StartIndex = startIdx;
                Me = me;
                Game = game;
                Moves = new List<PlayItOutResults>();
                Index = idx;
                var bclone = CloneBoard(board);
                bclone.Occupy(movePlayer, idx);

                this.MoveCount++;

				//Check if it's a win
                WinPlayer = bclone.Winner();
                if (WinPlayer != null)
                {
                    if (WinPlayer == Me) 
                        Status = GameWinStatus.Win;
                    else 
                        IsLoss = true;
                    return;
                }

				// Check if it's a tie
                if (bclone.IsFull())
                {
                    Status = GameWinStatus.Tie;
                    return;
                }

                // invert move player
                var newMovePlayer = movePlayer == Game.Player1 ? Game.Player2 : Game.Player1;

                for (var i = 0; i < 9; i++)
                {
                    if (!bclone.IsPositionOccupied(i))
                    {
                        var res = new PlayItOutResults(StartIndex,i, Me, newMovePlayer, bclone, Game, Focus, MoveCount);
                        Moves.Add(res);
                    }
                }
            }

            internal GameBoard CloneBoard(GameBoard board)
            {
                var bclone = new GameBoard();
                for (var row = 0; row < GameBoard.Height; row++)
                {
                    for (var p = 0; p < GameBoard.Width; p++)
                    {
                        bclone.BoardPositions[row][p] = board.BoardPositions[row][p];
                    }
                }
                return bclone;
            }

            internal int NextMove()
            {
                var results = GetEndResult();
                if (Focus == GameWinStatus.Tie)
                {
                    var winResults =
                        results
                            .OrderBy(x => x.MoveCount)
							.ThenBy(x => x.Status)
                            .GroupBy(x => x.StartIndex)
                            .Select(
                                x =>
                                    new
                                    {
                                        WinCount = x.Count(y => y.Status == GameWinStatus.Win),
                                        TieCount = x.Count(y => y.Status == GameWinStatus.Tie),
										LossCount = x.Count(y=>y.IsLoss),
										MoveCount = x.Count(),
                                        Results = x
											.OrderBy(y=>y.MoveCount)
                                            .ThenByDescending(y=>y.Status)//Descending because .Tie == 2 which is greater than .Win
                                            .ToArray()
                                    })
							.OrderBy(x=>x.MoveCount)
                            .ThenBy(x => x.LossCount)
							.ThenByDescending(x=>x.TieCount)
                            .ThenBy(x => x.WinCount)
                            .ToArray();
                    return winResults.First().Results.First().StartIndex;
                }
                if (this.Focus == GameWinStatus.Win)
                {
                    var winResults =
                        results
                            .GroupBy(x => x.StartIndex)
                            .Select(
                                x =>
                                    new
                                    {
                                        WinCount = x.Count(y => y.Status == GameWinStatus.Win),
                                        TieCount = x.Count(y => y.Status == GameWinStatus.Tie),
										LossCount = x.Count(y=>y.IsLoss),
										MoveCount = x.Count(),
                                        Results = x
											.OrderBy(y=>y.MoveCount)
                                            .ThenBy(y=>y.Status)//Ascending because .Win == 1 which is less than than .Win
                                            .ToArray()
                                    })
							.OrderBy(x=>x.MoveCount)
                            .ThenBy(x => x.LossCount)
                            .ThenByDescending(x => x.WinCount)
							.ThenBy(x=>x.TieCount)
                            .ToArray();

                    var wr = results
                        .OrderBy(x => x.MoveCount)
                        .ThenBy(x => x.IsLoss)
                        .ThenByDescending(x => x.Status)
                        .ToArray();

                    //var nextWin = wr.FirstOrDefault(x => x.Status == GameWinStatus.Win);
                    //var nextTie = wr.FirstOrDefault(x => x.Status == GameWinStatus.Tie);
                    //var nextLoss = wr.FirstOrDefault(x => x.IsLoss);
                    
                    //List of losses
                    var lossList = wr.Where(x => x.IsLoss).ToArray();
                    // Start Index's to ignore because they'll kill us. 
                    var ignoreList = lossList.Where(x => x.MoveCount == 2).Select(x => x.StartIndex).Distinct().ToArray();
                    // Items that don't have start index's on the ignoreList
                    var passedThresholdList= wr.Where(x => ignoreList.Contains(x.StartIndex) == false).ToArray();

                    var nonLosses = passedThresholdList.Where(x => x.IsLoss == false).ToArray();
                    if(nonLosses.Length > 0)
                        return nonLosses[0].StartIndex;
                    return wr.First().StartIndex;
                }
				throw new InvalidOperationException("Can not set the focus to None");
            }

            internal List<PlayItOutResults> GetEndResult()
            {
                return GetEndResult(this.Moves);
            }

            internal List<PlayItOutResults> GetEndResult(List<PlayItOutResults> moves)
            {
                var ret = new List<PlayItOutResults>();
                foreach (var m in moves)
                {
                    if (m.Status != GameWinStatus.None)
                    {
                        ret.Add(m);
                    }
                    else
                    {
                        if (m.IsLoss) ret.Add(m);
                        else ret.AddRange(GetEndResult(m.Moves));
                    }
                }
                return ret;
            }
        }
    }
}