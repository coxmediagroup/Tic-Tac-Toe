import functools
import unittest

from google.appengine.ext import testbed
import webtest

from fixture import GoogleDatastoreFixture
from fixture.loadable.google_datastore_loadable import EntityMedium
from fixture.style import NamedDataStyle

from main import app

__all__ = ("with_data", "KapxCMSBaseTestCase")


def with_data(datasets, models):
    """Decorate testcase methods and load the `datasets` before
    
    running the test
    """
    def decorator(test_func):
        @functools.wraps(test_func)
        def inner_wrapper(self):
            _datasets = datasets
            if isinstance(datasets, basestring):
                import sys
                mod = sys.modules[self.__class__.__module__]
                _datasets = getattr(mod, datasets)
            data = _load_data_sets(models, _datasets)
            test_func(self)
            data.teardown()
        return inner_wrapper
    return decorator


class KapxCMSBaseTestCase(unittest.TestCase):
    """Base class for all our tests"""
    
    def setUp(self):
        self.testbed = _testbed = testbed.Testbed()
        self.testbed.setup_env(
            USER_EMAIL='test@example.com',
            USER_ID='123',
            USER_IS_ADMIN='1',
            overwrite=True
        )
        _testbed.activate()
        _testbed.init_memcache_stub()
        _testbed.init_user_stub()
        _testbed.init_datastore_v3_stub()
        # the bare wsgi app under test (no wrapper around)
        self.target_app = app
        self.testapp = webtest.TestApp(app)

    def tearDown(self):
        self.testbed.deactivate()


class _NDBEntityMedium(EntityMedium):
    
    def _entities_to_keys(self, mylist):
        """Converts an array of datastore objects to an array of keys.
        
        if the value passed in is not a list, this passes it through as is
        """
        if type(mylist) is list:
            if all(map(lambda x: hasattr(x,'key'), mylist)):
                return [ent.key for ent in mylist]
        return mylist

    def clear(self, obj):
        """Delete this entity from the Datastore"""
        obj.key.delete()


def _load_data_sets(models, datasets):
    datafixture = GoogleDatastoreFixture(
        env=models,
        style=NamedDataStyle(),
        medium=_NDBEntityMedium
    )
    data = datafixture.data(*datasets)
    data.setup()
    return data