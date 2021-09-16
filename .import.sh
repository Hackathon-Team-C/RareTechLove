#!/bin/sh

docker-compose exec django ./manage.py import_slack 
