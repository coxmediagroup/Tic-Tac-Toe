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
        self.assertIn('Test Home', body.text)

        # TODO: use the admin site to create a Poll
        self.fail('finish this test')

