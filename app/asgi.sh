#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'
workers=24
sock=/var/run/app/asgi.sock
loglevel=error #Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'.

if [ "$1" = "--runserver" ]; then
    uvicorn asgi:application --host 0.0.0.0 --port 8000 --reload --ws websockets
else
    rm $sock
    uvicorn asgi:application --uds $sock --log-level $loglevel --workers $workers --ws websockets
fi
