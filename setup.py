#!/usr/bin/env python
import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-tictactoe',
    version='0.1.0',
    packages=[
        'tictactoe',
        'game',
        'game.tests',
        'game.migrations'
    ],
    url='https://github.com/paulcwatts/django-tictactoe',
    license='BSD',
    author='Paul Watts',
    author_email='paulcwatts@gmail.com',
    description='Django Tic-Tac-Toe game',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
