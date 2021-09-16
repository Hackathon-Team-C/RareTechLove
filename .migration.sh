#!/bin/sh

docker-compose exec django python3 manage.py makemigrations raretechloveapp
docker-compose exec django python3 manage.py migrate auth
docker-compose exec django python3 manage.py migrate --noinput
docker-compose exec django python3 manage.py collectstatic --no-input
