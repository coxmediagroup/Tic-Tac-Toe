from django.test import TestCase
from tic_tac_toe_play import is_final, has_winner

class UtilTestCase(TestCase):
    def setUp(self):
        pass

    def test_is_final(self):
        self.assertFalse(is_final([['x', 'o', 'x'],
                                   ['x', 'o', 'x'],
                                   ['x', 'o', 'e']]))
        self.assertTrue(is_final([['x', 'o', 'x'],
                                  ['x', 'x', 'x'],
                                  ['x', 'o', 'o']]))

    def test_has_winner_true(self):
        states = [
             ([['x', 'e', 'o'],
               ['o', 'x', 'x'],
               ['e', 'e', 'x']],
              [['X', 'e', 'o'],
               ['o', 'X', 'x'],
               ['e', 'e', 'X']]),

             ([['x', 'e', 'o'],
               ['o', 'o', 'x'],
               ['o', 'e', 'x']],
              [['x', 'e', 'O'],
               ['o', 'O', 'x'],
               ['O', 'e', 'x']]),

             ([['o', 'o', 'o'],
               ['x', 'o', 'e'],
               ['o', 'e', 'x']],
              [['O', 'O', 'O'],
               ['x', 'o', 'e'],
               ['o', 'e', 'x']]),

             ([['o', 'o', 'e'],
               ['x', 'x', 'x'],
               ['o', 'e', 'x']],
              [['o', 'o', 'e'],
               ['X', 'X', 'X'],
               ['o', 'e', 'x']]),

             ([['o', 'o', 'e'],
               ['e', 'e', 'x'],
               ['o', 'o', 'o']],
              [['o', 'o', 'e'],
               ['e', 'e', 'x'],
               ['O', 'O', 'O']]),

             ([['o', 'o', 'e'],
               ['o', 'e', 'x'],
               ['o', 'e', 'o']],
              [['O', 'o', 'e'],
               ['O', 'e', 'x'],
               ['O', 'e', 'o']]),

             ([['x', 'x', 'e'],
               ['o', 'x', 'x'],
               ['o', 'x', 'o']],
              [['x', 'X', 'e'],
               ['o', 'X', 'x'],
               ['o', 'X', 'o']]),

             ([['x', 'e', 'o'],
               ['o', 'x', 'o'],
               ['e', 'e', 'o']],
              [['x', 'e', 'O'],
               ['o', 'x', 'O'],
               ['e', 'e', 'O']])
               ]

        for state, winning_state in states:
            self.assertTrue(has_winner(state))
            self.assertEqual(state, winning_state)


    def test_has_winner_false(self):
        from copy import deepcopy
        states = [
            [['e', 'e', 'e'],
             ['o', 'x', 'x'],
             ['e', 'o', 'e']],
            [['x', 'x', 'o'],
             ['o', 'x', 'x'],
             ['x', 'o', 'o']],
            ]

        for state in states:
            _state = deepcopy(state)
            self.assertFalse(has_winner(state))
            self.assertEqual(state,_state)
