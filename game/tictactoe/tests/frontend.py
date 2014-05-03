import time

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from nose.tools import eq_
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class TestFrontEnd(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        super(TestFrontEnd, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(TestFrontEnd, self).tearDown()

    def test_home(self):
        self._go_to('')
        home_link = self.driver.find_element_by_css_selector('.active')
        WebDriverWait(self.driver, 9).until(lambda driver: home_link)
        eq_(home_link.text, 'Home')

    def test_play_computer_wins(self):
        """Computer starts and wins the game"""
        # Load home page
        self._go_to('')

        # Make sure we find the 'Computer start' link
        computer_start = self.driver.find_element_by_link_text('Computer start')
        eq_(computer_start.text, 'Computer start')
        computer_start.click()
        time.sleep(0.5)

        # Human moves
        for mv in [1, 5]:
            move = self.driver.find_element_by_id('move_%s' % mv)
            WebDriverWait(self.driver, 9).until(lambda driver: move)
            move.click()

        time.sleep(0.75)
        alert_box = self.driver.find_element_by_css_selector('.alert-box')
        WebDriverWait(self.driver, 9).until(lambda driver: alert_box)
        # Assert computer wins
        eq_(alert_box.text, u'I win. Better luck next time! Click on the '
            'links above to play again.')

    def test_play_tie(self):
        self._go_to('%s?start=human' % reverse('tictactoe.play'))
        for mv in [0, 2, 7, 3, 5]:
            self.driver.find_element_by_id('move_%s' % mv).click()
            self.driver.implicitly_wait(9)

        alert_box = self.driver.find_element_by_css_selector('.alert-box')
        WebDriverWait(self.driver, 9).until(lambda driver: alert_box)
        eq_(alert_box.text, u"It's a tie. You almost got me that time! Click "
            "on the links above to play again.")
        time.sleep(0.75)

    def _go_to(self, url):
        self.driver.get(self.live_server_url + url)
        self.driver.implicitly_wait(9)
