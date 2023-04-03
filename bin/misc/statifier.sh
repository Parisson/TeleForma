#!/bin/bash

DOMAIN=$1

mkdir $DOMAIN
cd $DOMAIN

LANG=en
wget -q --mirror -p --adjust-extension --header='Accept-Language: en' -e robots=off --base=./ -k -P ./ https://$DOMAIN
mv $DOMAIN $LANG
find $LANG/ -type f -print0 | xargs -0 sed -r -i -e 's,<form action="https://'"$DOMAIN"'/i18n/" method="post" class="c-header__languages">,,g'
find $LANG/ -type f -print0 | xargs -0 sed -r -i -e 's,<button class="c-header__language" type="submit" name="language" value="fr">FR</button>,<a href="/fr/"><button class="c-header__language\" type="button" name="language" value="fr">FR \&nbsp\;</button></a>,g'
find $LANG/ -type f -print0 | xargs -0 sed -r -i -e 's,<button class="c-header__language is-active" type="submit" name="language" value="en">EN</button></form>,<a href="/en/"><button class="c-header__language\" type="button" name="language" value="en">\&nbsp\; EN</button></a>,g'

LANG=fr
wget -q --mirror -p --adjust-extension --header='Accept-Language: fr' -e robots=off --base=./ -k -P ./ https://$DOMAIN
mv $DOMAIN $LANG
find $LANG -type f -print0 | xargs -0 sed -r -i -e 's,<form action="https://'"$DOMAIN"'/i18n/" method="post" class="c-header__languages">,,g'
find $LANG -type f -print0 | xargs -0 sed -r -i -e 's,<button class="c-header__language is-active" type="submit" name="language" value="fr">FR</button>,<a href="/fr/"><button class="c-header__language\" type="button" name="language" value="fr">FR \&nbsp\;</button></a>,g'
find $LANG -type f -print0 | xargs -0 sed -r -i -e 's,<button class="c-header__language" type="submit" name="language" value="en">EN</button></form>,<a href="/en/"><button class="c-header__language\" type="button" name="language" value="en">\&nbsp\; EN</button></a>,g'
