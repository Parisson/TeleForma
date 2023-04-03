#!/bin/bash

# Exit when any command fails
# We need to stop build if pip fails
set -e

for module in `ls /srv/lib/`; do
	cd /srv/lib/$module
	if [ -f 'requirements.txt' ]; then
		pip3 install -r requirements.txt
	elif [ -f 'setup.py' ]; then
		pip3 install -e .
	fi
done
