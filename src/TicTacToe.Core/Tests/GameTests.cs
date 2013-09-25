namespace TicTacToe.Core.Tests
{
    using System;
    using System.Linq;
    using System.Threading;

    using FakeItEasy;

    using NUnit.Framework;

    using TicTacToe.Core.Actions;

    public class GameTests
    {
        private static Game BasicGame()
        {
            var h1 = new HumanPlayer("jim");
            var h2 = new HumanPlayer("tim");
            var game = new Game(h1, h2);
            return game;
        }

        [Test]
        public void Constructor_FillsClass()
        {
            var h1 = new HumanPlayer("jim");
            var h2 = new HumanPlayer("tim");
            using (var game = new Game(h1, h2))
            {
                Assert.NotNull(game.Board);
                Assert.AreEqual(h1, game.Player1);
                Assert.AreEqual(h2, game.Player2);
                Assert.NotNull(game.GameLog);
                Assert.NotNull(game.GameActions);
                Assert.AreEqual(GameStatus.Running, game.Status);
                Assert.AreEqual(GameWinStatus.None, game.WinStatus);
                Assert.Null(game.Winner);
                Assert.Null(game.PlayerTurn);
            }
        }

        [Test]
        public void Constructor_Constraints()
        {
            var tplayer = new HumanPlayer("jim");
            Assert.Throws<ArgumentException>(() => new Game(null, null));
            Assert.Throws<ArgumentException>(() => new Game(tplayer, null));
            Assert.Throws<ArgumentException>(() => new Game(null, tplayer));
        }

        [Test]
        public void Reset_FillsClass()
        {
            using (var game = BasicGame())
            {
                game.Status = GameStatus.Finished;
                game.WinStatus = GameWinStatus.Win;
                game.Winner = game.Player1;
                game.Board = null;
                game.Reset();
                Assert.AreEqual(GameStatus.Running, game.Status);
                Assert.AreEqual(GameWinStatus.None, game.WinStatus);
                Assert.Null(game.Winner);
                Assert.Null(game.PlayerTurn);
                Assert.NotNull(game.Board);
            }
        }

        [Test]
        public void Start_SetsTurnPlayerNext()
        {
            using (var game = BasicGame())
            {
                Assert.Null(game.PlayerTurn);
                game.Start();
                var cp = game.PlayerTurn;
            }
        }

        [Test]
        public void PerformAction_CantPassNullAction()
        {
            using(var game = BasicGame())
				Assert.Throws<ArgumentOutOfRangeException>(() => game.PerformAction(null));
        }

        [Test]
        public void PerformAction_CanOnlyDoResetOnFinishedGame()
        {
            using (var game = BasicGame())
            {
                game.Status = GameStatus.Finished;

                var occupyGameAction = new OccupyGameAction(game, game.Player1, 1, 1);
                Assert.Throws<InvalidOperationException>(() => game.PerformAction(occupyGameAction));

                var resetGameAction = new ResetGameAction(game, game.Player1);
                Assert.DoesNotThrow(() => game.PerformAction(resetGameAction));
                game.Status = GameStatus.Running;
                occupyGameAction.Player = game.PlayerTurn;
                Assert.DoesNotThrow(() => game.PerformAction(occupyGameAction));
            }
        }

        [Test]
        public void PerformAction_CantGoIfNotTurn()
        {
            using (var game = BasicGame())
            {
                var testAction =
                    A.Fake<GameAction>(x => x.WithArgumentsForConstructor(new object[] { game, game.Player1 }));
                game.PlayerTurn = game.Player2;
                Assert.Throws<InvalidOperationException>(() => game.PerformAction(testAction));
            }
        }

        [Test]
        public void PerformAction_EnqueusAction()
        {
            using (var game = BasicGame())
            {
                game.Start();
                var testAction =
                    A.Fake<GameAction>(x => x.WithArgumentsForConstructor(new object[] { game, game.PlayerTurn }));
                var num = 0;
                game.PerformAction(testAction);
                Assert.AreEqual(1, game.ActionQueue.Count);
            }
        }

        [Test]
        public void CheckGameState_SetsWin()
        {
            using (var game = BasicGame())
            {
                game.Board.BoardPositions[0][0] = game.Player1;
                game.Board.BoardPositions[1][0] = game.Player1;
                game.Board.BoardPositions[2][0] = game.Player1;

                game.GameActions.Add(new OccupyGameAction(game, game.Player1, 0, 0));
                game.GameActions.Add(new OccupyGameAction(game, game.Player2, 0, 1));

                Assert.Null(game.Winner);
                Assert.AreEqual(GameStatus.Running, game.Status);
                Assert.AreEqual(GameWinStatus.None, game.WinStatus);

                game.CheckGameState();

                Assert.AreEqual(game.Player1, game.Winner);
                Assert.AreEqual(GameStatus.Finished, game.Status);
                Assert.AreEqual(GameWinStatus.Win, game.WinStatus);
            }
        }

        [Test]
        public void CheckGameState_SetsTie()
        {
            using (var game = BasicGame())
            {
                Assert.Null(game.Winner);
                Assert.AreEqual(GameStatus.Running, game.Status);
                Assert.AreEqual(GameWinStatus.None, game.WinStatus);

				game.GameActions.Add(new OccupyGameAction(game,game.Player1,0,0));
                game.GameActions.Add(new OccupyGameAction(game, game.Player2, 0, 1));

                game.Board.BoardPositions[0][0] = game.Player1;
                game.Board.BoardPositions[1][0] = game.Player2;
                game.Board.BoardPositions[2][0] = game.Player1;
                game.Board.BoardPositions[0][1] = game.Player2;
                game.Board.BoardPositions[1][1] = game.Player1;
                game.Board.BoardPositions[2][1] = game.Player1;
                game.Board.BoardPositions[0][2] = game.Player2;
                game.Board.BoardPositions[1][2] = game.Player1;
                game.Board.BoardPositions[2][2] = game.Player2;

                game.CheckGameState();

                Assert.Null(game.Winner);
                Assert.AreEqual(GameStatus.Finished, game.Status);
                Assert.AreEqual(GameWinStatus.Tie, game.WinStatus);
            }
        }
    }
}