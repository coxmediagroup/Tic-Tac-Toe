import json

import django.core.urlresolvers
import django.test

from . import views


class TicTacToeViewTest(django.test.TestCase):
    """Tests for TicTacToe server responses."""

    def setUp(self):
        self.request_factory = django.test.client.RequestFactory()

    def test_renders_nine_board_cells(self):
        """Nine cells with appropriate IDs are rendered."""
        request = self.request_factory.get('')

        response = views.show_game(request)
        response_body = response.content.decode()

        for row_num in range(3):
            for col_num in range(3):
                self.assertIn("board-cell-{}-{}".format(row_num, col_num),
                              response_body)


class HandleMoveTest(django.test.TestCase):
    """Tests for the handle_move AJAX view."""

    def setUp(self):
        self.ai_url = django.core.urlresolvers.reverse(views.handle_move)

    def test_new_board_contains_old_board(self):
        """All taken cells are maintained when the AI responds."""
        board = json.dumps([
            'X  ',
            '   ',
            '   ',
        ])

        resp = self.client.post(self.ai_url, data=board,
                                content_type="application/json")
        response = json.loads(resp.content.decode())
        response_board = response['board']
        response_state = response['state']

        self.assertEqual([
            'X  ',
            ' O ',
            '   ',
        ], response_board)
        self.assertEqual("INCOMPLETE", response_state)

    def test_tells_game_state(self):
        """The server tells the client the new game state."""

        # the AI should finish the draw game
        board = json.dumps([
            'XOO',
            'OXX',
            'XXO',
        ])

        resp = self.client.post(self.ai_url, data=board,
                                content_type="application/json")
        response = json.loads(resp.content.decode())
        response_state = response['state']

        self.assertEqual("DRAW", response_state)