﻿namespace TicTacToe.Core.Tests
{
    using System;
    using System.Linq;

    using FakeItEasy;

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
        public void PerformAction_CanOnlyDoResetOnFinishedGame()
        {
            var game = Game();
            game.Status = GameStatus.Finished;

            var occupyGameAction = new OccupyGameAction(game.Player1, game, 1, 1);
            Assert.Throws<InvalidOperationException>(() => game.PerformAction(occupyGameAction));

            var passTurnGameAction = new PassTurnGameAction(game, game.Player1);
            Assert.Throws<InvalidOperationException>(() => game.PerformAction(passTurnGameAction));

            var resetGameAction = new ResetGameAction(game, game.Player1);
            Assert.DoesNotThrow(() => game.PerformAction(resetGameAction));
            occupyGameAction.Player = game.PlayerTurn;
            Assert.DoesNotThrow(() => game.PerformAction(occupyGameAction));
            passTurnGameAction.Player = game.PlayerTurn;
            Assert.DoesNotThrow(() => game.PerformAction(passTurnGameAction));
        }

        [Test]
        public void PerformAction_CantGoIfNotTurn()
        {
            var game = Game();
            var testAction = A.Fake<GameAction>(x=>x.WithArgumentsForConstructor(new object[]{game,game.Player1}));
            game.PlayerTurn = game.Player2;
            Assert.Throws<InvalidOperationException>(() => game.PerformAction(testAction));
        }

        [Test]
        public void PerformAction_SavesAction()
        {
            var game = Game();
            var action = new ResetGameAction(game, game.Player1);
            Assert.AreEqual(0, game.GameActions.Count);
            game.PerformAction(action);
            Assert.AreEqual(1, game.GameActions.Count);
        }

        [Test]
        public void PerformAction_CallsActionDo()
        {
            var game = Game();
            var testAction = A.Fake<GameAction>(x=>x.WithArgumentsForConstructor(new object[]{game,game.Player1}));
            var num = 0;
            A.CallTo(() => testAction.Do()).Invokes(() => num++);
            game.PerformAction(testAction);
            Assert.AreEqual(1, num);
        }

        [Test]
        public void PerformAction_CallsCheckGameState()
        {
            var game = Game();
            var testAction = A.Fake<GameAction>(x => x.WithArgumentsForConstructor(new object[] { game, game.Player1 }));

            game.PlayerTurn = game.Player1;

            game.Board.BoardPositions[0][0] = game.Player1;
            game.Board.BoardPositions[1][0] = game.Player1;
            game.Board.BoardPositions[2][0] = game.Player1;

            game.PerformAction(testAction);

            Assert.AreEqual(GameStatus.Finished, game.Status);
        }
    }
}