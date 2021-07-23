#!/bin/bash

python manage.py wait_for_database -s 0
python manage migrate
python manage collectstatic --noinput
uwsgi --ini uwsgi.ini
