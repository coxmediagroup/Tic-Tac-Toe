namespace TicTacToe.Core.Tests.Actions
{
	using NUnit.Framework;

	using TicTacToe.Core.Actions;

    public class ResetGameActionTests
    {
        [Test]
        public void Consturctor_SetsClass()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            var game = new Game(p1, p2);
            var action = new ResetGameAction(game,p1);

            Assert.AreEqual(p1, action.Player);
            Assert.AreEqual(game, action.Game);
        }

        [Test]
        public void Do_DoesReset()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            var game = new Game(p1, p2);
            var action = new ResetGameAction(game,p1);
            
			game.Status = GameStatus.Finished;
			action.Do();
            Assert.AreEqual(GameStatus.Running, game.Status);

        }

        [Test]
        public void Do_DoesLog()
        {
            var p1 = new HumanPlayer("jim");
            var p2 = new HumanPlayer("tim");
            var game = new Game(p1, p2);
            var action = new ResetGameAction(game,p1);

			Assert.AreEqual(0,game.GameLog.Count);
            action.Do();
            Assert.AreEqual(1, game.GameLog.Count);
        }
    }
}