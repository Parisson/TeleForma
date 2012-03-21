#!/bin/sh

./manage.py schemamigration teleforma --auto
./manage.py migrate teleforma

