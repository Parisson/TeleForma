#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'
workers=8
sock=/var/run/app/asgi.sock
loglevel=error #Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'.

if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000
else
    # static files auto update
    # watchmedo shell-command --patterns="$patterns" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $app &
    #daphne -b 0.0.0.0 -p 8000 asgi:application
    
    rm $sock

    uvicorn asgi:application --uds $sock --log-level $loglevel --workers $workers --ws websockets
fi


