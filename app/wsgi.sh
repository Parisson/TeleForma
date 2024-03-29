#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'
uwsgi_log='/var/log/uwsgi/app.log'
debug_log='/var/log/app/debug.log'

# patterns='*.js;*.css;*.jpg;*.jpeg;*.gif;*.png;*.svg;*.ttf;*.eot;*.woff;*.woff2'

# Install a package in development mode
# without rebuidling docker image.
# You need at first checkout your sources in 'lib' folder
# in host project side, then run :
# pip install -e /srv/lib/mypackage...
# pip3 install -U uwsgi

# Install (staging) libs
# /srv/bin/build/local/setup_lib.sh

# waiting for other services
sh $app/wait.sh

# django setup
#python $manage wait-for-db

# initial setup
# if [ ! -f .init ]; then
#     bash $app/bin/init.sh
#     touch .init
# fi

# app start
if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000 --noasgi
else
    # static files auto update
    # watchmedo shell-command --patterns="$patterns" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $app &

    python $manage collectstatic --noinput

    chown -R www-data: $debug_log

    uwsgi /srv/app/wsgi.ini
fi
