from setuptools import setup, find_packages

version = "0.1"

setup(
    name="tickytack",
    url="",
    author="Cris Ewing",
    author_email="cris@crisewing.com",
    license="",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    description="A simple tic-tac-toe game.  You won't win",
    long_description=open("README.rst").read(),
    install_requires=[
        'setuptools',
    ],
    classifiers=[
        'Framework :: Django',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)