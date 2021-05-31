#!/bin/sh

/srv/bin/misc/wait-for-it/wait-for-it.sh -h $DB_HOST -p $DB_PORT;
