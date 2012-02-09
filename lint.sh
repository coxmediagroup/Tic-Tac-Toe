#!/bin/sh

echo
echo

# Ignore line too long errors, personal preference
pep8 --ignore=E501 tictactoe

pylint --rcfile=pylint.rc tictactoe

echo
