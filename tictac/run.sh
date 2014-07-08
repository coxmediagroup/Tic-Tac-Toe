#!/usr/bin/env bash

export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=tictac.settings.dev

./apps/flask/websocktoe/websocktoe.py &
./manage.py runserver 

