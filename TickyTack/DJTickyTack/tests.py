from django.contrib.auth.models import User
from django.test.client import Client
from django.test.testcases import TestCase
from DJTickyTack.models import Game
import urls

class BaseTest(TestCase):
    """
    Defines a shared test fixture.
    """
    def setUp(self):
        create = User.objects.create_user
        self.player1 = create('player1', 'player1@example.com', 'pw1')
        self.player2 = create('player2', 'player2@example.com', 'pw2')

class GameTest(BaseTest):
    def test_construct(self):
        """
        A Game is a match between two players, started on a particular date.
        """
        game = Game(player1=self.player1, player2=self.player2)

        # player 1 to play
        self.assertEquals(self.player1, game.toPlay)

        # auto-populate the date on save
        self.assertEquals(None, game.startedOn)
        game.save()
        self.assertNotEqual(None, game.startedOn)



class SiteTest(BaseTest):

    def setUp(self):
        super(SiteTest, self).setUp()
        self.game = Game(player1=self.player1, player2=self.player2)
        self.game.save()
        self.client = Client()
        self.client.login(username='player1', password='pw1')


    def test_home(self):
        c = self.client
        r = c.get(urls.kHome)
        self.assertEquals(1, len(r.context['activeGames']))
