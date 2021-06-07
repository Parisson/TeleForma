#!/bin/sh

/srv/bin/misc/wait-for-it/wait-for-it.sh -h $DB_HOST -p $DB_PORT;
/srv/bin/misc/wait-for-it/wait-for-it.sh -h redis -p 6379;
