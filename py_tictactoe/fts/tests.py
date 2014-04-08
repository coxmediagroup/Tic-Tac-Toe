from django.test import LiveServerTestCase
from selenium import webdriver

class TicTacToeTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home(self):
        # Mary opens her web browser, and goes to the index page
        self.browser.get(self.live_server_url + '')

        # She sees the response
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Play TIC - TAC - TOE', body.text)

        self.browser.find_element_by_id('player-name').value("David")
        self.browser.find_element_by_id('player-first').click().submit()

    def test_play(self):
        # Mary starts a game
        self.browser.get(self.live_server_url + '/play?player-name=Mary&player-first=on')

        # She sees the response
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Mary, it is your turn', body.text)
