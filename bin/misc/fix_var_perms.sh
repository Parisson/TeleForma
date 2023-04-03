#!/bin/bash

cd "$(dirname "$0")"/../../

# We need to chown folders so that they can be used by the $USER (with an exception on Darwin)
if ! uname -a | grep Darwin > /dev/null; then

    declare -a arr=("var/media" "var/backup")

    for folder in "${arr[@]}"; do
        INFO=( $(stat -L -c "%a %G %U" $folder) )
        OWNER=${INFO[2]}
        if [ "$OWNER" != "$USER" ]; then
            sudo chown -R $USER $folder
        fi
    done
fi
