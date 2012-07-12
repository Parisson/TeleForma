#!/bin/sh

./manage.py schemamigration teleforma --auto
./manage.py schemamigration telemeta --auto
./manage.py schemamigration telecaster --auto
./manage.py migrate

