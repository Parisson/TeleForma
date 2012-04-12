#!/bin/sh

app="teleforma"

dir="../doc"

./manage.py graph_models -a > $dir/$app-all.dot
./manage.py graph_models $app > $dir/$app.dot

dot $dir/$app-all.dot -Tpdf -o $dir/$app-all.pdf
dot $dir/$app.dot -Tpdf -o $dir/$app.pdf

rsync -a $dir/ doc.parisson.com:/var/www/files/doc/$app/diagram/
