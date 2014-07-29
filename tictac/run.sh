#!/usr/bin/env bash

export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=tictac.settings.dev

function _cleanup() {
    # Kill all child processes of current process
    pids=$(pgrep -f `which python`)
    echo $pids | xargs kill -TERM
}

# Run flask websocket server
python ./apps/flask/websocktoe/websocktoe.py &

# Run Django server
python ./manage.py runserver

# Cleanup once Django server exits
_cleanup
