import django.test

from . import views


class TicTacToeViewTest(django.test.TestCase):
    """Tests for TicTacToe server responses."""

    def setUp(self):
        self.request_factory = django.test.client.RequestFactory()

    def test_renders_nine_board_cells(self):
        """Nine cells with appropriate IDs are rendered."""
        request = self.request_factory.get('')

        response = views.say_hello(request)
        response_body = response.content.decode()

        for row_num in range(3):
            for col_num in range(3):
                self.assertIn("board-cell-{}-{}".format(row_num, col_num), response_body)