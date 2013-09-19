namespace TicTacToe.Core.Tests
{
    using System;
    using System.Linq;

    using NUnit.Framework;

    using TicTacToe.Core.Actions;

    public class GameTests
    {
        private Game Game()
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
            var game = new Game(h1, h2);
            Assert.NotNull(game.Board);
            Assert.AreEqual(h1, game.Player1);
            Assert.AreEqual(h2, game.Player2);
            Assert.NotNull(game.GameLog);
            Assert.NotNull(game.GameActions);
            Assert.AreEqual(GameStatus.Running, game.Status);
            Assert.AreEqual(GameWinStatus.None, game.WinStatus);
            Assert.Null(game.Winner);
            Assert.NotNull(game.PlayerTurn);
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
            var game = Game();
            game.Status = GameStatus.Finished;
            game.WinStatus = GameWinStatus.Win;
            game.Winner = game.Player1;
            game.Board = null;
            game.Reset();
            Assert.AreEqual(GameStatus.Running, game.Status);
            Assert.AreEqual(GameWinStatus.None, game.WinStatus);
            Assert.Null(game.Winner);
            Assert.NotNull(game.PlayerTurn);
            Assert.NotNull(game.Board);
        }

        [Test]
        public void Reset_SetsTurnPlayerNext()
        {
            var game = Game();
            var cp = game.PlayerTurn;
            for (var i = 0; i < 10; i++)
            {
                game.Reset();
                Assert.AreNotEqual(cp, game.PlayerTurn);
                cp = game.PlayerTurn;
            }
        }

        [Test]
        public void PerformAction_CantPassNullAction()
        {
            var game = Game();
            Assert.Throws<ArgumentOutOfRangeException>(() => game.PerformAction(null));
        }

        [Test]
        public void PerformAction_CanOnlyDoResetOnFinsihedGame()
        {
            var game = Game();
            game.Status = GameStatus.Finished;

            var action = new OccupyGameAction(game.Player1, game, 1, 1);
            Assert.Throws<InvalidOperationException>(() => game.PerformAction(action));

            var action2 = new PassTurnGameAction(game, game.Player1);
            Assert.Throws<InvalidOperationException>(() => game.PerformAction(action2));

            var action3 = new ResetGameAction(game, game.Player1);
            Assert.DoesNotThrow(() => game.PerformAction(action3));

            Assert.DoesNotThrow(() => game.PerformAction(action));
            action2.Player = game.PlayerTurn;
            Assert.DoesNotThrow(() => game.PerformAction(action2));
        }
    }
}