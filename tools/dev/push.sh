#!/bin/bash

git branch | tr -d \* | while read line
do
    branch=${line/#\ }

    echo "Push $branch to origin:"
    git push origin $branch

done

git push --tags

ssh vcs.parisson.com "cd /var/git/teleforma.git; git update-server-info"

echo "Update sandbox @ angus.parisson.com:"
ssh angus.parisson.com "cd /home/teleforma/teleforma; git pull; \
                        cd /home/teleforma/teleforma-dev; git pull; \
                        cd /home/teleforma/sandbox/; ./manage.py migrate --delete-ghost-migrations; \
                        ./manage.py collectstatic "

echo "Done !"
