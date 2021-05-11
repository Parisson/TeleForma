#!/bin/sh

/srv/bin/misc/wait-for-it/wait-for-it.sh -h localhost -p $DB_PORT;
