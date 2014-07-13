#!/usr/bin/env bash

export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=tictac.settings.dev

function _cleanup() {
    pids=$(pgrep -f `which python`)
    echo $pids | xargs kill -TERM
}

# Run flask websocket server in background
./apps/flask/websocktoe/websocktoe.py &

# Run Django server in background
./manage.py runserver &

sleep 3

# Run tests
./manage.py test -v1 --settings=tictac.settings.test

# Cleanup once tests finish
_cleanup
