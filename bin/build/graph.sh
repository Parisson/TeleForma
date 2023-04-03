#!/bin/sh

docker-compose run app python /srv/app/manage.py graph_models organization-core organization-media organization-pages organization.network organization.magazine organization.projects organization.agenda organization.shop organization.job > /srv/doc/graph/mezzanine-organization.dot
