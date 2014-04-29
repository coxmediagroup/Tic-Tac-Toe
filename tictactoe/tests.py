from django.test import TestCase
from . import validators, models
from django.core.exceptions import ValidationError


class FrontEndTestCase(TestCase):
    def test_everything_via_karma(self):
        import subprocess, os
        old_dir = os.getcwd()
        try:
            dname = os.path.split(__file__)[0]

            os.chdir(dname)
            code = subprocess.call("static/tictactoe/ng/"
                    "node_modules/karma/bin/karma start karma.conf.js", 
                    shell=True)
            self.assertEqual(0, code)

        finally:
            os.chdir(old_dir)

class ValidatorTests(TestCase):
    def test_x_or_o(self):
        self.assertTrue(validators.is_x_or_o('X') is None) 
        self.assertTrue(validators.is_x_or_o('O') is None) 
        self.assertRaises(ValidationError, lambda:validators.is_x_or_o('A')) 


class GameTests(TestCase):
    def test_detect_row_1_wins(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='A1') #  X
        g.moves.create(cell='A3') #  O
        g.moves.create(cell='B1') #  X
        g.moves.create(cell='B3') #  O
        g.moves.create(cell='C1') #  X
        self.assertEqual(g.winner, 'X')

    def test_detect_row_2_wins(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='A3') #  X
        g.moves.create(cell='A2') #  O
        g.moves.create(cell='B1') #  X
        g.moves.create(cell='B2') #  O
        g.moves.create(cell='C1') #  X
        g.moves.create(cell='C2') #  O
        self.assertEqual(g.winner, 'O')

    def test_detect_row_3_wins(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='A2') #  X
        g.moves.create(cell='A3') #  O
        g.moves.create(cell='B1') #  X
        g.moves.create(cell='B3') #  O
        g.moves.create(cell='C1') #  X
        g.moves.create(cell='C3') #  O
        self.assertEqual(g.winner, 'O')

    def test_detect_col_A_win(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='A1') #  X
        g.moves.create(cell='C3') #  O
        g.moves.create(cell='A2') #  X
        g.moves.create(cell='B3') #  O
        g.moves.create(cell='A3') #  X
        self.assertEqual(g.winner, 'X')

    def test_detect_col_B_win(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='B1') #  X
        g.moves.create(cell='C3') #  O
        g.moves.create(cell='B2') #  X
        g.moves.create(cell='A3') #  O
        g.moves.create(cell='B3') #  X
        self.assertEqual(g.winner, 'X')

    def test_detect_col_C_win(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='C1') #  X
        g.moves.create(cell='B3') #  O
        g.moves.create(cell='C2') #  X
        g.moves.create(cell='A3') #  O
        g.moves.create(cell='C3') #  X
        self.assertEqual(g.winner, 'X')

    def test_detect_diag_win_1(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='A1') #  X
        g.moves.create(cell='B3') #  O
        g.moves.create(cell='B2') #  X
        g.moves.create(cell='A3') #  O
        g.moves.create(cell='C3') #  X
        self.assertEqual(g.winner, 'X')

    def test_detect_diag_win_2(self):
        g = models.Game(ip='127.0.0.1', player='X')
        g.save()
        g.moves.create(cell='A3') #  X
        g.moves.create(cell='B3') #  O
        g.moves.create(cell='B2') #  X
        g.moves.create(cell='A2') #  O
        g.moves.create(cell='C1') #  X
        self.assertEqual(g.winner, 'X')