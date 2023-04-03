#!/bin/sh

docker-compose exec -T app python /srv/app/manage.py build-front $1
