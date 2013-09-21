namespace TicTacToe.Core.Tests
{
    using System.IO;

    using NUnit.Framework;
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
    }
}