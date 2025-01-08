#!/bin/bash
rm db.sqlite3
rm -r ./**/migrations
python manage.py makemigrations model
python manage.py migrate
