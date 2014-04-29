from django.test import TestCase

class FrontEndTestCase(TestCase):
    def test_everything_via_karma(self):
        import subprocess, os
        old_dir = os.getcwd()
        try:
            dname = os.path.split(__file__)[0]

            os.chdir(dname)
            code = subprocess.call("static/tictactoe/ng/"
                    "node_modules/karma/bin/karma start karma.conf.js", 
                    shell=True)
            self.assertEqual(0, code)

        finally:
            os.chdir(old_dir)