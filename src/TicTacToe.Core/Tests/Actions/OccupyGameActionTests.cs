namespace TicTacToe.Core.Tests.Actions
{
    using System;

    using NUnit.Framework;

    using TicTacToe.Core.Actions;

    public class OccupyGameActionTests
    {
        [Test]
        public void Consturctor_SetsClass()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            using (var game = new Game(p1, p2))
            {
                var action = new OccupyGameAction(game, p1, 2, 1);

                Assert.AreEqual(p1, action.Player);
                Assert.AreEqual(game, action.Game);
                Assert.AreEqual(2, action.X);
                Assert.AreEqual(1, action.Y);
            }
        }

        [Test]
        public void Constructor_Constraints()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            using (var game = new Game(p1, p2))
            {
                Assert.Throws<ArgumentException>(() => new OccupyGameAction(game, p1, 12, 0));
                Assert.Throws<ArgumentException>(() => new OccupyGameAction(game, p1, 0, 12));
            }
        }

        [Test]
        public void Do_ThrowsIfPositionOccupiedAlready()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            using (var game = new Game(p1, p2))
            {
                var action = new OccupyGameAction(game, p1, 2, 1);

                Assert.DoesNotThrow(action.Do);
                Assert.Throws<InvalidOperationException>(action.Do);
            }
        }

        [Test]
        public void Do_OccupiesSpaceCorrectly()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            using (var game = new Game(p1, p2))
            {
                var action = new OccupyGameAction(game, p1, 2, 1);

                action.Do();
                Assert.NotNull(game.Board.BoardPositions[1][2]);
                Assert.AreEqual(p1, game.Board.BoardPositions[1][2]);
            }
        }

        [Test]
        public void Do_DoesLog()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            using (var game = new Game(p1, p2))
            {
                var action = new OccupyGameAction(game, p1, 2, 1);

                Assert.AreEqual(0, game.GameLog.Count);
                action.Do();
                Assert.AreEqual(1, game.GameLog.Count);
            }
        }
    }
}