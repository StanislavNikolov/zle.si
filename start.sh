#!/bin/sh

uwsgi --socket 127.0.0.1:3031 --processes 1 --threads 1 --need-plugin python3 --wsgi-file main.py
