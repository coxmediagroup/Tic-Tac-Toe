# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import requests

from splinter import Browser

from django.conf import settings
from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from apps.coxtactoe import const as C

import logging
log = logging.getLogger(__name__)


class CoxtactoeEndToEndTests(LiveServerTestCase):
    browser = None

    def __init__(self, *args, **kwargs):
        super(CoxtactoeEndToEndTests, self).__init__(*args, **kwargs)
        try:
            self.base_url = settings.BASE_URL
        except AttributeError:
            host = os.environ.get('HOSTNAME')
            self.base_url = 'http://%s:%s' % (host, '8000')
        self.splash_url = "{}{}".format(self.base_url, reverse(
            C.VIEW_NAME_SPLASH, urlconf='apps.coxtactoe.urls'))

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser(settings.SELENIUM_WEBDRIVER)
        super(CoxtactoeEndToEndTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(CoxtactoeEndToEndTests, cls).tearDownClass()

    def _get_full_url(self, url_path):
        return ''.join([self.base_url, url_path])

    def _test_splash_page_click(self, button):
        self.browser.visit(self.splash_url)
        self.assertTrue(self.browser.is_text_present('TACTOE'))
        self.browser.find_by_id(button).click()
        self.assertTrue(self.browser.is_text_present('Game Log', wait_time=5))
        return True

    def _test_xo_choice_matches_player(self, player):
        xo_choice = self.browser.evaluate_script(
            'angular.element("body").scope().xo_choice')
        self.assertEquals(xo_choice, player)

    def _test_clicking_xo_on_game_page_starts_new_game_as_xo(self, player):
        button = player.lower()
        self.assertTrue(self._test_splash_page_click(button))
        old_game_id = self.browser.url.split('/')[-1]
        self.browser.find_by_id(button).click()
        self.assertTrue(
            self.browser.is_text_not_present(old_game_id, wait_time=5))
        self._test_xo_choice_matches_player(player)

    def test_splash_page_load(self):
        self.browser.visit(self.splash_url)
        self.assertTrue(self.browser.is_text_present('TACTOE'))
        self.assertTrue(self.browser.is_text_present('Pick X or O above'))

    def test_clicking_x_on_splash_page_starts_new_game_as_x(self):
        self.assertTrue(self._test_splash_page_click('x'))
        self._test_xo_choice_matches_player('X')

    def test_clicking_o_on_splash_page_starts_new_game_as_o(self):
        self.assertTrue(self._test_splash_page_click('o'))
        self._test_xo_choice_matches_player('O')

    def test_clicking_x_on_game_page_starts_new_game_as_x(self):
        self._test_clicking_xo_on_game_page_starts_new_game_as_xo('X')

    def test_clicking_o_on_game_page_starts_new_game_as_o(self):
        self._test_clicking_xo_on_game_page_starts_new_game_as_xo('O')

    def test_socketio_connected(self):
        self.assertTrue(self._test_splash_page_click('x'))
        self.assertTrue(
            self.browser.is_text_present('[recv] msg: Connected', wait_time=5))

    def test_socketio_joined(self):
        self.assertTrue(self._test_splash_page_click('x'))
        self.assertTrue(
            self.browser.is_text_present('[recv] msg: Joined', wait_time=5))

    def test_http_response_on_invalid_xo_choice(self):
        data = {'xo_choice': 'z'}
        headers = {}
        for cookie in self.browser.cookies.all():
            headers[cookie['name']] = cookie['value']
        response = requests.post(self.splash_url, data=data, headers=headers)
        self.assertGreaterEqual(response.status_code, 400)
