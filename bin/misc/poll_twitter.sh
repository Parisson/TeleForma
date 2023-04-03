#!/bin/sh

docker-compose exec -T app python /srv/app/manage.py poll_twitter --force
