from django.test import TestCase

# Create your tests here.
class FrontEndTestCase(TestCase):
    def test_everything_via_karma(self):
        import subprocess
        code = subprocess.call("static/ng/node_modules/karma/bin/karma start karma.conf.js", shell=True)
        self.assertEqual(0, code)