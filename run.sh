#!/bin/bash

python manage.py wait_for_database -s 0
uwsgi --ini uwsgi.ini