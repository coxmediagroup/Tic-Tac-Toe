namespace TicTacToe.Core.Tests
{
    using System;
    using System.IO;

    using NUnit.Framework;

    using TicTacToe.Core.Actions;

    public class LearnProcessorTests
    {
        [Test]
        public void Constructor_FillsAndCreatesFile()
        {
			var fname = System.IO.Path.GetTempFileName();
            try
            {
                File.Delete(fname);
                var lp = new LearnProcessor(fname);
                Assert.True(File.Exists(fname));
                Assert.AreEqual(fname, lp.LearnFile);
                Assert.NotNull(lp.CacheList);

				// Check to make sure it loads up the longs

				File.WriteAllLines(fname,new []{"1","2","3"});

                lp = new LearnProcessor(fname);

				Assert.IsNotEmpty(lp.CacheList);
                Assert.AreEqual(1, lp.CacheList[0]);
                Assert.AreEqual(2, lp.CacheList[1]);
                Assert.AreEqual(3, lp.CacheList[2]);
            }
            finally
            {
                File.Delete(fname);
            }
        }

        [Test]
        public void ProcessEndGame_Constraints()
        {
            var fname = Path.GetTempFileName();
            try
            {
                var p1 = new HumanPlayer("jim");
                var p2 = new HumanPlayer("tim");
                var game = new Game(p1, p2);
                var lp = new LearnProcessor(fname);

				//Blows up because game isn't over
                Assert.Throws<InvalidOperationException>(() => lp.ProcessEndGame(game));

				game.Status = GameStatus.Finished;

				// Blows up because WinStatus of game isn't set right
                Assert.Throws<InvalidOperationException>(() => lp.ProcessEndGame(game));
				
            }
            finally
            {
                File.Delete(fname);
            }
        }

        [Test]
        public void ProcessEndGame_AddsToListAndSaves()
        {
            var fname = Path.GetTempFileName();
            try
            {
                var p1 = new HumanPlayer("jim");
                var p2 = new HumanPlayer("tim");
                var game = new Game(p1, p2);
				game.GameActions.Add(new OccupyGameAction(game,p1,0,1));
                game.GameActions.Add(new OccupyGameAction(game, p2, 0, 2));
				game.Status = GameStatus.Finished;
				game.WinStatus = GameWinStatus.Win;
                var lp = new LearnProcessor(fname);

				lp.ProcessEndGame(game);
                Assert.AreEqual(1, lp.CacheList.Count);

                var lp2 = new LearnProcessor(fname);
                Assert.AreEqual(1, lp2.CacheList.Count);

                Assert.AreEqual(lp.CacheList[0], lp2.CacheList[0]);

                lp.ProcessEndGame(game);
                Assert.AreEqual(1, lp.CacheList.Count);

                lp2 = new LearnProcessor(fname);
                Assert.AreEqual(1, lp2.CacheList.Count);

                Assert.AreEqual(lp.CacheList[0], lp2.CacheList[0]);
            }
            finally
            {
                File.Delete(fname);
            }
        }
    }
}