from setuptools import setup, find_packages

package_data = []
dependencies = []
setup(name="tictactoe",
      version="0.0.1",
      description="A simple tic tac toe game",
      author="Justin Michalicek",
      author_email="jmichalicek@gmail.com",
      license="www.opensource.org/licenses/bsd-license.php",
      packages=find_packages(),
      package_data={'tictactoe' : package_data },
      install_requires=dependencies,
      long_description='A simple tic tac toe game',
      test_suite='tests')
