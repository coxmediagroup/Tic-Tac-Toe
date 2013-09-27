namespace TicTacToe.Core.Tests.Utils
{
	using NUnit.Framework;

	using Core.Utils;

    public class RngRandomTests
    {
        [Test]
        public void Next_min_max__PicksCorrectRange()
        {
            for (var i = 0; i < 10000; i++)
            {
                var num = RngRandom.Instance.Next(0, 2);
				Assert.GreaterOrEqual(num,0);
				Assert.LessOrEqual(num,1);
				Assert.AreNotEqual(2,num);
                Assert.AreNotEqual(-1, num);
            }
        }
    }
}