#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'

if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000
else
    # static files auto update
    # watchmedo shell-command --patterns="$patterns" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $app &
    daphne -b 0.0.0.0 -p 8000 asgi:application
fi


