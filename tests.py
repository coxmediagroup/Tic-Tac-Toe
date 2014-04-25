#!/usr/bin/env python

from tictactoe import app

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

class FlaskTestCase(unittest.TestCase):
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
            response = tester.post('/board', data={'layout':
                                                       '[["X", " ", " "], '
                                                       '[" ", " ", " "], '
                                                       '[" ", " ", " "]]'})

            board = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(count_total_moves(board), 1)


if __name__ == '__main__':
    unittest.main()
