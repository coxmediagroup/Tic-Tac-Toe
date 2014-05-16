#!/usr/bin/env python

from tictactoe import app
from game import Board

from copy import copy
import json
import lxml.html
import os
import tempfile
import unittest

def get_initial_board(response):
    html = lxml.html.fromstring(response.data)
    return json.loads(html.find(".//div[@id='board']").get('board_layout'))

def count_total_moves(data):
    counter = 0
    for row in data:
        for column in row:
            if column != " ":
                counter += 1

    return counter

class TestUrl(unittest.TestCase):
    def test_tic_tac_toe(self):
        with app.test_client() as tester:
            response = tester.get('/')
            self.assertEqual(response.status_code, 200)

    def test_tic_tac_toe_board(self):
        with app.test_client() as tester:
            response = tester.get('/?player-first')
            self.assertEqual(response.status_code, 200)
            board = get_initial_board(response)
            self.assertEqual(board, [[u" ", u" ", u" "],
                                     [u" ", u" ", u" "],
                                     [u" ", u" ", u" "]])

            self.assertEqual(count_total_moves(board), 0)
            test_board_1 = ('[["X", " ", " "], '
                            '[" ", " ", " "], '
                            '[" ", " ", " "]]')

            test_board_2 = ('[["X", "O", "O"], '
                            '["O", "X", "X"], '
                            '["X", "X", "O"]]')

            test_board_3 = ('[["X", "X", "X"], '
                            '["X", "O", "O"], '
                            '[" ", "O", " "]]')

            response = tester.post('/board', data={'layout': test_board_1})
            board = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(count_total_moves(board), 1)

            url = '/is-draw?layout={}'.format(test_board_2)
            response = tester.get(url)
            self.assertEqual(response.status_code, 200)
            is_draw = False if response.data == 'False' else True
            self.assertEqual(is_draw, True)

            url = '/is-win?layout={}'.format(test_board_2)
            response = tester.get(url)
            self.assertEqual(response.status_code, 200)
            winner = None if response.data == '' else response.data
            self.assertEqual(winner, None)

            url = '/is-win?layout={}'.format(test_board_3)
            response = tester.get(url)
            self.assertEqual(response.status_code, 200)
            winner = None if response.data == '' else response.data
            self.assertEqual(winner, 'player')

            url = '/ai-move?layout={}'.format(test_board_1)
            response = tester.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.data, test_board_1)

class AiTest(unittest.TestCase):
    def test_center(self):
        start_board = ('[[" ", " ", " "], '
                        '[" ", " ", " "], '
                        '[" ", " ", " "]]')

        ai_move = ('[[" ", " ", " "], '
                   '[" ", "O", " "], '
                   '[" ", " ", " "]]')



        with app.test_client() as tester:
            url = '/ai-move?layout={}'.format(start_board)
            response = tester.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, ai_move)

    def test_opposite_corner(self):
        moves = (
            ('[[" ", " ", "X"], '
               '["O", "X", " "], '
               '[" ", " ", " "]]',
             '[[" ", " ", "X"], '
                '["O", "X", " "], '
                '["O", " ", " "]]'),

            ('[[" ", " ", " "], '
               '["O", "X", " "], '
               '["X", " ", " "]]',
             '[[" ", " ", "O"], '
                '["O", "X", " "], '
                '["X", " ", " "]]'),

            ('[[" ", " ", " "], '
               '["O", "X", " "], '
               '[" ", " ", "X"]]',
             '[["O", " ", " "], '
                '["O", "X", " "], '
                '[" ", " ", "X"]]'),

            ('[[" ", " ", "X"], '
               '["O", "X", " "], '
               '[" ", " ", " "]]',
             '[[" ", " ", "X"], '
                '["O", "X", " "], '
                '["O", " ", " "]]'),
            )


        with app.test_client() as tester:
            for start_board, ai_move in moves:
                url = '/ai-move?layout={}'.format(start_board)
                response = tester.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, ai_move)

    def test_any_corner(self):
        moves = (
            ('[[" ", "?", "?"], '
               '["?", "?", "?"], '
               '["?", "?", "?"]]',
            '[["O", "?", "?"], '
               '["?", "?", "?"], '
               '["?", "?", "?"]]'),

            ('[["?", "?", " "], '
               '["?", "?", "?"], '
               '["?", "?", "?"]]',
            '[["?", "?", "O"], '
               '["?", "?", "?"], '
               '["?", "?", "?"]]'),

            ('[["?", "?", "?"], '
               '["?", "?", "?"], '
               '["?", "?", " "]]',
            '[["?", "?", "?"], '
               '["?", "?", "?"], '
               '["?", "?", "O"]]'),

            ('[["?", "?", "?"], '
               '["?", "?", "?"], '
               '[" ", "?", "?"]]',
            '[["?", "?", "?"], '
               '["?", "?", "?"], '
               '["O", "?", "?"]]'),
            )


        with app.test_client() as tester:
            for start_board, ai_move in moves:
                url = '/ai-move?layout={}'.format(start_board)
                response = tester.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, ai_move)

    def test_any_side(self):
        moves = (
            ('[["?", " ", "?"], '
               '["?", "?", "?"], '
               '["?", "?", "?"]]',
            '[["?", "O", "?"], '
               '["?", "?", "?"], '
               '["?", "?", "?"]]'),

            ('[["?", "?", "?"], '
               '["?", "?", " "], '
               '["?", "?", "?"]]',
            '[["?", "?", "?"], '
               '["?", "?", "O"], '
               '["?", "?", "?"]]'),

            ('[["?", "?", "?"], '
               '["?", "?", "?"], '
               '["?", " ", "?"]]',
            '[["?", "?", "?"], '
               '["?", "?", "?"], '
               '["?", "O", "?"]]'),

            ('[["?", "?", "?"], '
               '[" ", "?", "?"], '
               '["?", "?", "?"]]',
            '[["?", "?", "?"], '
               '["O", "?", "?"], '
               '["?", "?", "?"]]'),
            )


        with app.test_client() as tester:
            for start_board, ai_move in moves:
                url = '/ai-move?layout={}'.format(start_board)
                response = tester.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, ai_move)

    def test_win(self):
        moves = (
            ('[["O", "O", " "], '
               '["X", " ", " "], '
               '[" ", " ", "X"]]',
              '[["O", "O", "O"], '
               '["X", " ", " "], '
               '[" ", " ", "X"]]'),

            ('[["O", " ", "O"], '
               '["X", " ", " "], '
               '[" ", " ", "X"]]',
              '[["O", "O", "O"], '
               '["X", " ", " "], '
               '[" ", " ", "X"]]'),

            ('[[" ", "O", "O"], '
               '["X", " ", " "], '
               '[" ", " ", "X"]]',
              '[["O", "O", "O"], '
               '["X", " ", " "], '
               '[" ", " ", "X"]]'),

            ('[["X", " ", "O"], '
              '[" ", " ", "O"], '
              '[" ", "X", " "]]',
             '[["X", " ", "O"], '
              '[" ", " ", "O"], '
              '[" ", "X", "O"]]'),

            ('[["X", " ", " "], '
              '[" ", "X", "O"], '
              '[" ", " ", "O"]]',
             '[["X", " ", "O"], '
              '[" ", "X", "O"], '
              '[" ", " ", "O"]]'),

            ('[["X", " ", "O"], '
              '[" ", "X", " "], '
              '[" ", " ", "O"]]',
             '[["X", " ", "O"], '
              '[" ", "X", "O"], '
              '[" ", " ", "O"]]'),

            ('[[" ", "X", " "], '
              '["O", "O", " "], '
              '["X", " ", " "]]',
             '[[" ", "X", " "], '
              '["O", "O", "O"], '
              '["X", " ", " "]]'),

            ('[[" ", "X", " "], '
              '["O", " ", "O"], '
              '["X", " ", " "]]',
             '[[" ", "X", " "], '
              '["O", "O", "O"], '
              '["X", " ", " "]]'),

            ('[[" ", "X", " "], '
              '[" ", "O", "O"], '
              '["X", " ", " "]]',
             '[[" ", "X", " "], '
              '["O", "O", "O"], '
              '["X", " ", " "]]'),

            ('[[" ", " ", " "], '
              '["X", " ", "X"], '
              '["O", "O", " "]]',
             '[[" ", " ", " "], '
              '["X", " ", "X"], '
              '["O", "O", "O"]]'),

            ('[[" ", " ", " "], '
              '["X", " ", "X"], '
              '["O", " ", "O"]]',
             '[[" ", " ", " "], '
              '["X", " ", "X"], '
              '["O", "O", "O"]]'),

            ('[[" ", " ", " "], '
              '["X", " ", "X"], '
              '[" ", "O", "O"]]',
             '[[" ", " ", " "], '
              '["X", " ", "X"], '
              '["O", "O", "O"]]'),

            ('[["O", " ", " "], '
              '["X", "O", "X"], '
              '[" ", " ", " "]]',
             '[["O", " ", " "], '
              '["X", "O", "X"], '
              '[" ", " ", "O"]]'),

            ('[["O", " ", " "], '
              '["X", " ", "X"], '
              '[" ", " ", "O"]]',
             '[["O", " ", " "], '
              '["X", "O", "X"], '
              '[" ", " ", "O"]]'),

            ('[[" ", " ", " "], '
              '["X", "O", "X"], '
              '[" ", " ", "O"]]',
             '[["O", " ", " "], '
              '["X", "O", "X"], '
              '[" ", " ", "O"]]'),

            ('[[" ", " ", "O"], '
              '["X", "O", "X"], '
              '[" ", " ", " "]]',
             '[[" ", " ", "O"], '
              '["X", "O", "X"], '
              '["O", " ", " "]]'),

            ('[[" ", " ", "O"], '
              '["X", " ", "X"], '
              '["O", " ", " "]]',
             '[[" ", " ", "O"], '
              '["X", "O", "X"], '
              '["O", " ", " "]]'),

            ('[[" ", " ", " "], '
              '["X", "O", "X"], '
              '["O", " ", " "]]',
             '[[" ", " ", "O"], '
              '["X", "O", "X"], '
              '["O", " ", " "]]'),
          )


        with app.test_client() as tester:
            for start_board, ai_move in moves:
                url = '/ai-move?layout={}'.format(start_board)
                response = tester.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, ai_move)

    def test_fork(self):
        moves = (
            ('[[" ", "O", " "], '
              '["X", "X", "O"], '
              '["O", " ", " "]]',
             '[[" ", "O", "O"], '
              '["X", "X", "O"], '
              '["O", " ", " "]]'),

            ('[[" ", "O", " "], '
              '["O", "X", "X"], '
              '[" ", " ", " "]]',
             '[["O", "O", " "], '
              '["O", "X", "X"], '
              '[" ", " ", " "]]'),

            ('[[" ", "O", " "], '
              '["O", "X", "X"], '
              '[" ", "O", " "]]',
             '[[" ", "O", " "], '
              '["O", "X", "X"], '
              '["O", "O", " "]]'),

            ('[["O", " ", " "], '
              '["X", "X", "O"], '
              '[" ", "O", " "]]',
             '[["O", " ", " "], '
              '["X", "X", "O"], '
              '[" ", "O", "O"]]'),
          )


        with app.test_client() as tester:
            for start_board, ai_move in moves:
                url = '/ai-move?layout={}'.format(start_board)
                response = tester.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, ai_move)

class BoardTest(unittest.TestCase):
    def test_board(self):
        blank_board = {0: {0: " ", 1: " ", 2: " "},
                       1: {0: " ", 1: " ", 2: " "},
                       2: {0: " ", 1: " ", 2: " "}
                     }
        test_board = {0: {0: "X", 1: " ", 2: "O"},
                      1: {0: " ", 1: "X", 2: "O"},
                      2: {0: "O", 1: " ", 2: "X"}
                     }

        board = Board()
        self.assertEqual(board.board(), blank_board)
        board = Board(setup=test_board)
        self.assertEqual(board.board(), test_board)
        for x in range(0, 3):
            for y in range(0, 3):
                self.assertEqual(board.square((x, y)),
                                 board.board()[x][y])
        test_board2 = Board(setup=copy(blank_board))
        for i in range(0, 3):
            test_board2.square((i, i), set_to="X")

        for coords in ((0, 2), (1, 2), (2, 0)):
            test_board2.square(coords, set_to="O")

        self.assertEqual(test_board2.board(), test_board)
        self.assertEqual(board.check_requirements(
                         [[0, 0], [1, 1], [2,2]], {"X": 3}), True)
        self.assertEqual(board.check_requirements(
                         [[0, 2], [1, 2], [2,2]], {"O": 3}), False)
        self.assertEqual(board.traverse(requires={"O": 3}), [])
        self.assertEqual(board.traverse(requires={"O": 2}), [
            [(0, 2), (1, 2), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]])

if __name__ == '__main__':
    #unittest.main()
    from unittest import TestResult
    from unittest import TestSuite
    from unittest import TextTestRunner
    result = TestResult()
    runner = TextTestRunner()
    fast = TestSuite()
    fast.addTest(AiTest('test_fork'))
    runner.run(fast)

