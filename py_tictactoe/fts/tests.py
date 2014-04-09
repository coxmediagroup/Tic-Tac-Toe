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

        self.browser.find_element_by_class_name('toggle-button').click()
        self.browser.find_element_by_id('player-name').send_keys("Mary")

    def test_play(self):
        # Mary starts a game
        self.browser.get(self.live_server_url + '')

        self.browser.find_element_by_class_name('toggle-button').click()
        self.browser.find_element_by_id('player-name').send_keys("Mary")

        self.browser.find_element_by_tag_name('button').click()

        # She sees the response
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Mary, Good Luck', body.text)
        self.assertIn('Player 1 (X): Mary', body.text)

        self.browser.find_element_by_id('cell_1').click()

