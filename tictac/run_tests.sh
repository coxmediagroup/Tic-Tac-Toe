#!/usr/bin/env bash

export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=tictac.settings.dev
export FLASK_SETTINGS_MODULE=tictac.settings.flask.test

function _cleanup() {
    ws_pids=$(pgrep -f websocktoe.py)
    pids=$(pgrep -f `which python`)
    echo $ws_pids $pids | xargs kill -TERM
}

# Run flask websocket server in background
./apps/flask/websocktoe/websocktoe.py > flask_test.log 2>&1 &

# Run Django server in background
./manage.py runserver > django_test.log 2>&1 &

sleep 5

# Run tests
./manage.py test -v1 --settings=tictac.settings.test

# Cleanup once tests finish
_cleanup
