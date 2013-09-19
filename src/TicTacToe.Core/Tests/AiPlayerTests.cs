namespace TicTacToe.Core.Tests
{
    using NUnit.Framework;

    public class AiPlayerTests
    {
        [Test]
        public void Constructor_FillsClass()
        {
            var p = new AiPlayer("jim");
            Assert.AreEqual("jim", p.Name);
        }

        [Test]
        public void ToString_ReturnsName()
        {
            var p = new AiPlayer("jim");
            Assert.AreEqual("jim", p.ToString());
        }
    }
}