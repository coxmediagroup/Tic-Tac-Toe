# -*- coding: utf-8 -*-
"""
========================
Flask-KVSession Settings
========================

NOTE: These settings are imported by the base Flask config and will overwrite
      any settings of the same name which may be defined there.

``SESSION_KEY_BITS``
    The size of the random integer to be used when generating random session
    ids through generate_session_key().
    Defaults to 64.bit_length

``SESSION_RANDOM_SOURCE``
    An object supporting random.getrandbits(), used as a random source by the
    module. Defaults to an instance of random.SystemRandom.

``PERMANENT_SESSION_LIFETIME``
    When making a session permanent through KVSession.permanent, it will
    live this long (specified by a timedelta object).

``SECRET_KEY``
    The Flask SECRET_KEY is used to sign session ids that are stored in cookies
    in the users browser to making brute-force guessing a lot harder.

``SESSION_COOKIE_NAME``
    The same cookie name as Flask’s default session’s is used for
    server-side sessions.

"""
from datetime import timedelta


PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)