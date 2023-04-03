#!/bin/sh

docker-compose stop
mv data var
mkdir var/lib
sudo mv var/postgresql var/lib
sudo mv var/external var/opt
sudo mv var/var/log var
sudo rm -rf var/var
