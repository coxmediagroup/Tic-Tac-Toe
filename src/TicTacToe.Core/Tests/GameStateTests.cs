using TicTacToe.Core.Players.AI;

namespace TicTacToe.Core.Tests
{
    using System;
    using NUnit.Framework;

    using TicTacToe.Core.Actions;

    public class GameStateTests
    {
        [Test]
        public void Constructor_FillsClass()
        {
            var gs = new GameState();
            Assert.AreEqual(0, gs.MoveCount);
            Assert.Null(gs.Player1);
            Assert.Null(gs.Player2);
            Assert.Null(gs.Winner);
            Assert.NotNull(gs.MoveList);
        }

        [Test]
        public void Constructor_Game_Constraints()
        {
            var p1 = new HumanPlayer("a");
            var p2 = new HumanPlayer("b");
            using (var game = new Game(p1, p2))
            {
                Assert.Throws<InvalidOperationException>(() => new GameState(game));
                game.Status = GameStatus.Finished;
                Assert.Throws<InvalidOperationException>(() => new GameState(game));
                game.WinStatus = GameWinStatus.Tie;

                game.GameActions.Add(new OccupyGameAction(game, p1, 0, 0, 0));
                game.GameActions.Add(new OccupyGameAction(game, p2, 1, 0, 0));
                Assert.DoesNotThrow(() => new GameState(game));
            }
        }

        [Test]
        public void Constructor_Game_FillsClass()
        {
            var p1 = new HumanPlayer("a");
            var p2 = new HumanPlayer("b");
            using (var game = new Game(p1, p2))
            {
                game.Start(p2);
                game.GameActions.Add(new OccupyGameAction(game, p2, 0, 0, 0));
                game.GameActions.Add(new OccupyGameAction(game, p1, 1, 0, 0));
                game.Status = GameStatus.Finished;
                game.WinStatus = GameWinStatus.Tie;
                game.Winner = p1;

                var gs = new GameState(game);

                Assert.AreEqual(game.GameActions.Count, gs.MoveCount);
                Assert.AreEqual(game.GameActions.Count, gs.MoveList.Count);
                Assert.AreEqual(p2, gs.Player1);
                Assert.AreEqual(p1, gs.Player2);
                Assert.AreEqual(p1, gs.Winner);

                Assert.AreEqual(p2, gs.MoveList[0].Player);
                Assert.AreEqual(p1, gs.MoveList[1].Player);
            }
        }

        [Test]
        public void ToLong_FromLong()
        {
            var p1 = new HumanPlayer("a");
            var p2 = new HumanPlayer("b");
            using (var game = new Game(p1, p2))
            {
                game.Start(p2);
                game.GameActions.Add(new OccupyGameAction(game, p2, 0, 0, 0));
                game.GameActions.Add(new OccupyGameAction(game, p1, 1, 0, 0));
                game.Status = GameStatus.Finished;
                game.WinStatus = GameWinStatus.Tie;
                game.Winner = p1;

                var gs = new GameState(game);

                var state = GameState.ToLong(gs);

                Assert.AreNotEqual(0, state);

                var newgs = GameState.FromLong(state, p2, p1);

                Assert.AreEqual(gs.MoveCount, newgs.MoveCount);
                Assert.AreEqual(gs.Player1, newgs.Player1);
                Assert.AreEqual(gs.Player2, newgs.Player2);
                Assert.AreEqual(gs.Winner, newgs.Winner);

                for (var i = 0; i < gs.MoveList.Count; i++)
                {
                    Assert.AreEqual(gs.MoveList[i], newgs.MoveList[i]);
                }
            }
        }

        [Test]
        public void ToLongs()
        {
            var p1 = new HumanPlayer("a");
            var p2 = new HumanPlayer("b");
            using (var game = new Game(p1, p2))
            {
                game.Start(p2);
                var action1 = new OccupyGameAction(game, p2, 0, 0, 0);
                var action2 = new OccupyGameAction(game, p1, 1, 0, 0);

                game.GameActions.Add(action1);
                game.GameActions.Add(action2);
                game.Status = GameStatus.Finished;
                game.WinStatus = GameWinStatus.Tie;
                game.Winner = p1;

                var gs = new GameState(game);

                var longs = GameState.ToLongs(gs);

				// Hflip
                action1.X = 2;

                gs = new GameState(game);

                var gl = GameState.ToLong(gs);

                Assert.Contains(gl, longs);

				// Flip players
                game.StartPlayer = p1;
                action1.Player = p1;
                action2.Player = p2;
                game.Winner = p2;

                gs = new GameState(game);

                gl = GameState.ToLong(gs);

                Assert.Contains(gl, longs);

            }
        }
    }
}