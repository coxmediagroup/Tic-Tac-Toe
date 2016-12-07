using TicTacToe.Core.Players;

namespace TicTacToe.Core.Tests
{
    using NUnit.Framework;
    public class HumanPlayerTests
    {
        [Test]
        public void Constructor_FillsClass()
        {
            var p = new HumanPlayer("jim");
            Assert.AreEqual("jim", p.Name);
        }

        [Test]
        public void ToString_ReturnsName()
        {
            var p = new HumanPlayer("jim");
            Assert.AreEqual("jim", p.ToString());
        }
    }
}