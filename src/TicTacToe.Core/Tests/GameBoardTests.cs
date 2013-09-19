namespace TicTacToe.Core.Tests
{
    using System;

    using NUnit.Framework;
    public class GameBoardTests
    {
        [Test]
        public void Constructor_FillsClass()
        {
            var board = new GameBoard();
            Assert.AreEqual(3, board.BoardPositions.Length);
            foreach (var row in board.BoardPositions)
            {
				Assert.AreEqual(3, row.Length);
            }

            Assert.AreEqual(8, board.WinConditions.Length);
            foreach (var row in board.WinConditions)
            {
				Assert.AreEqual(3, row.Length);
            }
        }

        [Test]
        public void IsPositionOccupied_IsCorrect()
        {
            var board = new GameBoard();
            var p1 = new HumanPlayer("jim");

            Assert.False(board.IsPositionOccupied(1, 1));
            board.Occupy(p1, 1, 1);
            Assert.True(board.IsPositionOccupied(1, 1));
        }

        [Test]
        public void Occupy_SetsBoardPosition()
        {
            var board = new GameBoard();
            var p1 = new HumanPlayer("jim");

            Assert.False(board.BoardPositions[1][1] != null);
            board.Occupy(p1, 1, 1);
            Assert.True(board.BoardPositions[1][1] != null);
            Assert.AreEqual(p1, board.BoardPositions[1][1]);
        }

        [Test]
        public void Occupy_ThowsIfOccupied()
        {
            var board = new GameBoard();
            var p1 = new HumanPlayer("jim");

            board.Occupy(p1, 1, 1);
            Assert.Throws<InvalidOperationException>(() => board.Occupy(p1, 1, 1));
        }

        [Test]
        public void IsFull_IsCorrect()
        {
            var board = new GameBoard();
            var p1 = new HumanPlayer("jim");

            Assert.False(board.IsFull());

            board.BoardPositions[0][0] = p1;
            board.BoardPositions[1][0] = p1;
            Assert.False(board.IsFull());
            board.BoardPositions[2][0] = p1;
            board.BoardPositions[0][1] = p1;
            Assert.False(board.IsFull());
            board.BoardPositions[1][1] = p1;
            board.BoardPositions[2][1] = p1;
            Assert.False(board.IsFull());
            board.BoardPositions[0][2] = p1;
            board.BoardPositions[1][2] = p1;
            Assert.False(board.IsFull());
            board.BoardPositions[2][2] = p1;

            Assert.True(board.IsFull());
        }
    }
}